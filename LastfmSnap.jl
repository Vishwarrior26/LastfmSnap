using DataFrames
using Dates
using HTTP
using LightXML

#=
Get username
    If 200, good
    Else throw error
Get date range # TODO See if better way to do this than current method
Get number of items to process # TODO Unnecessary? May be faster to display truncated graph instead

With data, parse dates

Make some pretty graphs
Return DataFrame as CSV?
=#


"""
    getXML(username::String, page::Integer)

Gets XML response from Lastfm API for given username. Gets 200 tracks per page for processing.

Username should be well formatted, without leading or trailing whitespaces or anything of the kind.
"""
function getXML(username::String, page::Integer)
    baseUrl::String = "https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&format=xml&limit=200&api_key=959357ab2524c0d50de6e4ee8e792c68&user="
    try
        r = HTTP.get(baseUrl * username * "&page=" * page)
        xdoc = parse_string(String(r.body))
        return xdoc
    catch e
        println(e)
        println("Something's wrong; check your entered username or see if https://last.fm is down.")
    end
end

# TODO Delete?
function parseTrackXMLElement(track)
    dateTime = parse(DateTime, content(find_element(track, "date")), dateformat"dd u yyyy, HH:MM")
    trackTitle = content(find_element(track, "name"))
    album = content(find_element(track, "album"))
    artist = content(find_element(track, "artist"))
    return fill(dateTime, trackTitle, album, artist)
end

# TODO Delete?
function parseXMLPage(tracks)
    init = 1
    if has_attribute(tracks[1], "nowplaying")
        init = 2
    end
    return [parseTrackXMLElement(x) for x::XMLElement in tracks[init:end]]
end

"""
    getLastfmData(username::String, startDateTime::DateTime, endDateTime::DateTime)

Gets lastfm data for 'username' from startDateTime to endDateTime.

Assumes both values are in bounds (user has scrobbles in time frame)
"""
function getLastfmData(username::String, startDateTime::DateTime, endDateTime::DateTime)
    startDateTime < endDateTime ? nothing : startDateTime, endDateTime = endDateTime, startDateTime
    page = 1

    xdoc = getXML(username, page)
    tracks::Vector{XMLElement} = collect(child_elements(collect(child_elements(root(xdoc)))[1]))
    free(xdoc)
    if has_attribute(tracks[1], "nowplaying")
        popfirst!(tracks)
    end

    earliestTrackDate::DateTime = parseTrackXMLElement(tracks[end])[1]
    while earliestTrackDate > startDateTime

        xdoc = getXML(username, page)
        append!(tracks, collect(child_elements(collect(child_elements(root(xdoc)))[1])))
        free(xdoc)
        if has_attribute(tracks[1], "nowplaying")
            popfirst!(tracks)
        end

        earliestTrackDate::DateTime = parseTrackXMLElement(tracks[end])[1]
        if earliestTrackDate > startDateTime
            page += 1
        end
    end
end