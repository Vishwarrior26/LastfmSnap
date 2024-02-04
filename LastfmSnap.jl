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


print("Enter your username: \n")
username::String = "vishwarrior" # strip(readline())

function getXML(username::String)
    try
        r = HTTP.get(baseUrl * username)
        xdoc = parse_string(String(r.body))
        return xdoc
    catch e
        println(e)
        println("Something's wrong; check your entered username or see if https://last.fm is down.")
    end
end

# Function for pages beyond 1
getXML(username::String, page::Integer) = getXML(username * "&page=" * page)

xdoc = getXML(username)
xroot = root(xdoc)

tracks = collect(child_elements(collect(child_elements(xroot))[1]))

function parseTrackXMLElement(track)
    dateTime = parse(DateTime, content(find_element(track, "date")), dateformat"dd u yyyy, HH:MM")
    trackTitle = content(find_element(track, "name"))
    album = content(find_element(track, "album"))
    artist = content(find_element(track, "artist"))
    return fill(dateTime, trackTitle, album, artist)
end

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

If either is out of bounds, goes to nearest possible value.
"""
function getLastfmData(username::String, startDateTime::DateTime, endDateTime::DateTime)
    const baseUrl::String = "https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&format=xml&limit=200&api_key=959357ab2524c0d50de6e4ee8e792c68&user="

end