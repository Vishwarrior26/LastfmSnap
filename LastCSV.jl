using DataFrames, Dates, HTTP, LightXML, CSV


"""
    getXML(username, page)

Get XML response from Lastfm API for given username.
    
Gets 1000 tracks per page for processing. Username should be well formatted, without leading or trailing whitespaces or anything of the kind.
"""
function getXML(username, page)
    baseUrl::String = "https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&format=xml&limit=1000&api_key=959357ab2524c0d50de6e4ee8e792c68&user="
    try
        # Make request to API
        return parse_string(String(HTTP.get(baseUrl * username * "&page=" * string(page)).body))
    catch e
        println(e)
        println("Something's wrong; check your entered username or see if https://last.fm is down.")
    end
end

"""
    parseXMLPage!(scrobbles, xdoc)

Get the tracks associated with the given XML document and put them into `scrobbles`, mutating.

"""
function parseXMLPage!(scrobbles, xdoc)
    # Get track objects
    pageScrobbles = collect(child_elements(collect(child_elements(root(xdoc)))[1]))
    # Drop the first track if currently being scrobbled
    if has_attribute(pageScrobbles[1], "nowplaying")
        popfirst!(pageScrobbles)
    end
    # Append scrobbles to results list
    append!(scrobbles, pageScrobbles)
end

"""
    parseDate(scrobble)

Parse a date as given by the Last.fm API into a DateTime object. Times are in UTC.
"""
function parseDate(scrobble)
    return parse(DateTime, content(find_element(scrobble, "date")), dateformat"dd u yyyy, HH:MM")
end

"""
    parseTrackXMLElement(scrobble)

Extract information from a scrobble.
"""
function parseTrackXMLElement(scrobble)
    # Parses the XMLElement and gets appropriate information
    dateTime = parseDate(scrobble)
    trackTitle = content(find_element(scrobble, "name"))
    album = content(find_element(scrobble, "album"))
    artist = content(find_element(scrobble, "artist"))
    return (dateTime, trackTitle, album, artist)
end

"""
    getLastfmData(username)

Get all available last.fm data for this user. Returns a DataFrame.
"""
function getLastfmData(username)
    # Get first page for some basic processing
    xdoc = getXML(username, 1)
    totalPages = parse(Int64, attributes_dict(root(xdoc)["recenttracks"][1])["totalPages"])
    totalScrobbles = parse(Int64, attributes_dict(root(xdoc)["recenttracks"][1])["total"]) # total number of scrobbles of user

    # Initialize results list
    scrobbles = Vector{XMLElement}()
    sizehint!(scrobbles, totalScrobbles)

    # Process first page since request already made
    parseXMLPage!(scrobbles, xdoc)

    # Asynchronous multithreaded requests for major speedup
    @sync Threads.@threads for page = 2:totalPages
        @async parseXMLPage!(scrobbles, getXML(username, page))
    end

    df = DataFrame(parseTrackXMLElement.(scrobbles))
    return sort!(df)
end

# Driver code for CLI usage
username = ARGS[1]
CSV.write(username * ".csv", getLastfmData(username), header=["date", "track", "album", "artist"])
println("Wrote to " * username * ".csv")