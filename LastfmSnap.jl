using DataFrames, Dates, HTTP, LightXML

#=
Get username
    If 200, good
    Else throw error
Get date range # TODO See if better way to do this than current method

With data, parse dates

Make some pretty graphs?
Return DataFrame as CSV?
=#
const baseUrl::String = "https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&format=xml&limit=1000&api_key=959357ab2524c0d50de6e4ee8e792c68&user="

"""
    getXML(username::String, page::Integer)

Gets XML response from Lastfm API for given username. Gets 1000 tracks per page for processing.

Username should be well formatted, without leading or trailing whitespaces or anything of the kind.
"""
function getXML(username::String, page::Integer)
    try
        # TODO rewrite as async?
        return parse_string(String(HTTP.get(baseUrl * username * "&page=" * string(page)).body))
    catch e
        println(e)
        println("Something's wrong; check your entered username or see if https://last.fm is down.")
    end
end

function parseDate(track::XMLElement)
    return parse(DateTime, content(find_element(track, "date")), dateformat"dd u yyyy, HH:MM")
end

function parseXMLPage(tracks, xdoc, endDateTime)
    # TODO make check for max pages
    pageTracks = collect(child_elements(collect(child_elements(root(xdoc)))[1]))
    if has_attribute(pageTracks[1], "nowplaying")
        popfirst!(pageTracks)
    end
    pageStart = parseDate(pageTracks[end])
    if pageStart < endDateTime
        # println(pageStart)
        append!(tracks, pageTracks)
    end
    return parseDate(pageTracks[end])
end

"""
    getLastfmData(username::String, startDateTime::DateTime, endDateTime::DateTime)

Gets lastfm data for 'username' from startDateTime to endDateTime, inclusive on both ends.

Assumes both values are in bounds (user has scrobbles in time frame)
"""
function getLastfmData(username::String, startDateTime::DateTime, endDateTime::DateTime)
    # startDateTime < endDateTime ? nothing : startDateTime, endDateTime = endDateTime, startDateTime
    page = 1
    tracks = Vector{XMLElement}()
    xdoc = getXML(username, page)
    earliestTrackDate::DateTime = parseXMLPage(tracks, xdoc, endDateTime)
    while earliestTrackDate > startDateTime
        xdoc = getXML(username, page)
        earliestTrackDate = parseXMLPage(tracks, xdoc, endDateTime)
        if earliestTrackDate > startDateTime
            page += 1
        end
    end
    # TODO rewrite this to be more efficient
    df = DataFrame(
        date=[parseDate(track) for track in tracks],
        track=[content(find_element(track, "name")) for track in tracks],
        album=[content(find_element(track, "album")) for track in tracks],
        artist=[content(find_element(track, "artist")) for track in tracks]
    )
    # println(page)
    return subset(df, :date => d -> startDateTime .<= d .<= endDateTime)
end


function parseXMLPage(tracks, xdoc)
    pageTracks = collect(child_elements(collect(child_elements(root(xdoc)))[1]))
    if has_attribute(pageTracks[1], "nowplaying")
        popfirst!(pageTracks)
    end
    append!(tracks, pageTracks)
    free(xdoc)
end

"""
Get all available last.fm data for this user.
"""
function getLastfmData(username::String)
    xdoc = getXML(username, 1)
    totalPages = parse(Int64, attributes_dict(root(xdoc)["recenttracks"][1])["totalPages"])
    totalTracks = parse(Int64, attributes_dict(root(xdoc)["recenttracks"][1])["total"])
    tracks = Vector{XMLElement}()
    sizehint!(tracks, totalTracks)

    @sync Threads.@threads for page = 1:totalPages
        @async parseXMLPage(tracks, getXML(username, page))
    end

    df = DataFrame(parseTrackXMLElement.(tracks))

    return sort!(df)
end

function parseTrackXMLElement(track)
    dateTime = parse(DateTime, content(find_element(track, "date")), dateformat"dd u yyyy, HH:MM")
    trackTitle = content(find_element(track, "name"))
    album = content(find_element(track, "album"))
    artist = content(find_element(track, "artist"))
    return (dateTime, trackTitle, album, artist)
end

getLastfmData("vishwarrior")

using BenchmarkTools
# @btime getLastfmData("vishwarrior") 
# @btime getLastfmData("vishwarrior", DateTime(2023, 01, 01), DateTime(2024, 01, 01))
@btime getLastfmData("xchickenskinx")
@btime getLastfmData("xchickenskinx", DateTime(2023, 01, 01), DateTime(2024, 01, 01))