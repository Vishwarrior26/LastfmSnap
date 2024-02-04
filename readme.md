# LastfmSnap
LastfmSnap is a project designed to give last.fm users fine access to their data by helping them access snapshots of their listening history. Currently, the only supported function is a full extract of all last.fm data. Built in Julia, uses last.fm's API.

## Usage
`julia .\LastCSV.jl USERNAME_HERE`

Pass your username when calling LastCSV.jl to get a CSV of all your LastFM scrobbles, sorted chronologically. The field retrieved are date (with time), track, album, & artist.

OR

Use `getLastfmData(username)`  with your username and receive a DataFrame for further processing.

## TODO
* Make graphs
* Allow for custom paths to export data
* Optimize code
  * Better async requests?
  * Multiprocessing/threading broadcast for df creation?
  * Check typing
