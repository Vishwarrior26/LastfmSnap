using DataFrames, Dates, HTTP, LightXML, CSV, Distributed


"""
getXML(username, page)

Get XML response from Lastfm API for given username.
    
    Gets 1000 tracks per page for processing. Username should be well formatted, without leading or trailing whitespaces or anything of the kind.
        """
function getXML(username, page)
    baseUrl::String = "https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&format=xml&limit=1000&api_key=959357ab2524c0d50de6e4ee8e792c68&user="
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
function parseXMLPage!(scrobbles, xdoc)
    pageScrobbles = collect(child_elements(collect(child_elements(root(xdoc)))[1]))
    if has_attribute(pageScrobbles[1], "nowplaying")
        popfirst!(pageScrobbles)
    end
    append!(scrobbles, pageScrobbles)
end

"""
    parseDate(track)

Parse a date as given by the Last.fm API into a DateTime object. Times are in UTC.
"""
function parseDate(scrobble)
    return parse(DateTime, content(find_element(scrobble, "date")), dateformat"dd u yyyy, HH:MM")
end

function parseTrackXMLElement(scrobble)
    dateTime = parseDate(scrobble)
    trackTitle = content(find_element(scrobble, "name"))
    album = content(find_element(scrobble, "album"))
    artist = content(find_element(scrobble, "artist"))
    return (dateTime, trackTitle, album, artist)
end

"""
    getLastfmData(username)

Get all available last.fm data for this user.
"""
function getLastfmData(username)
    xdoc = getXML(username, 1)
    totalPages = parse(Int64, attributes_dict(root(xdoc)["recenttracks"][1])["totalPages"])
    totalScrobbles = parse(Int64, attributes_dict(root(xdoc)["recenttracks"][1])["total"])
    scrobbles = Vector{XMLElement}()
    sizehint!(scrobbles, totalScrobbles)
    parseXMLPage!(scrobbles, xdoc)

    @sync Threads.@threads for page = 2:totalPages
        @async parseXMLPage!(scrobbles, getXML(username, page))
    end

    dates = Vector{DateTime}(undef, totalScrobbles)
    tracks = Vector{String}(undef, totalScrobbles)
    albums = Vector{String}(undef, totalScrobbles)
    artists = Vector{String}(undef, totalScrobbles)

    Threads.@threads for i in 1:totalScrobbles
        scrobble = scrobbles[i]
        dates[i] = parseDate(scrobble)
        tracks[i] = content(find_element(scrobble, "name"))
        albums[i] = content(find_element(scrobble, "album"))
        artists[i] = content(find_element(scrobble, "artist"))
    end


    df = DataFrame(
        date=dates,
        track=tracks,
        album=albums,
        artist=artists
    )

    # df = DataFrame(parseTrackXMLElement.(scrobbles))
    return sort!(df)
end

using BenchmarkTools
@profview @btime getLastfmData("vishwarrior")
@profview @btime getLastfmData("vishwarrior")

username = ARGS[1]
CSV.write(username * ".csv", getLastfmData(username), header=["date", "track", "album", "artist"])
println("Wrote to " * username * ".csv")