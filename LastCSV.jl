using DataFrames, Dates, HTTP, LightXML, CSV

const baseUrl::String = "https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&format=xml&limit=1000&api_key=959357ab2524c0d50de6e4ee8e792c68&user="

"""
    getXML(username, page)

Get XML response from Lastfm API for given username.
    
Gets 1000 tracks per page for processing. Username should be well formatted, without leading or trailing whitespaces or anything of the kind.
"""
function getXML(username, page)
    try
        return parse_string(String(HTTP.get(baseUrl * username * "&page=" * string(page)).body))
    catch e
        println(e)
        println("Something's wrong; check your entered username or see if https://last.fm is down.")
    end
end

"""
    parseXMLPage!(tracks, xdoc)

Get the tracks associated with the given XML document and put them into `tracks`, modifying it in place.

"""
function parseXMLPage!(tracks, xdoc)
    pageTracks = collect(child_elements(collect(child_elements(root(xdoc)))[1]))
    if has_attribute(pageTracks[1], "nowplaying")
        popfirst!(pageTracks)
    end
    append!(tracks, pageTracks)
end

"""
    parseDate(track)

Parse a date as given by the Last.fm API into a DateTime object
"""
function parseDate(track)
    return parse(DateTime, content(find_element(track, "date")), dateformat"dd u yyyy, HH:MM")
end

function parseTrackXMLElement(track)
    dateTime = parseDate(track)
    trackTitle = content(find_element(track, "name"))
    album = content(find_element(track, "album"))
    artist = content(find_element(track, "artist"))
    return (dateTime, trackTitle, album, artist)
end

"""
    getLastfmData(username)

Get all available last.fm data for this user.
"""
function getLastfmData(username)
    xdoc = getXML(username, 1)
    totalPages = parse(Int64, attributes_dict(root(xdoc)["recenttracks"][1])["totalPages"])
    totalTracks = parse(Int64, attributes_dict(root(xdoc)["recenttracks"][1])["total"])
    tracks = Vector{XMLElement}()
    sizehint!(tracks, totalTracks)
    parseXMLPage!(tracks, xdoc)

    # Asynchronous multithreading to greatly speed up processing time 
    @sync Threads.@threads for page = 2:totalPages
        @async parseXMLPage!(tracks, getXML(username, page))
    end

    df = DataFrame(parseTrackXMLElement.(tracks))

    return sort!(df)
end

username = ARGS[1]
CSV.write(username * ".csv", getLastfmData(username), header=["date", "track", "album", "artist"])