Multi-section support in one file
Version tag in file
Search
     Add regex and case ignore options.
Make CSS import tolerant of flipped rel/href order
Config
   Include/Exclude
Format
   Status
   Attribution
Handle merge or conflict of sections
Private projects
Project or section generator
Option parsing
     Output filename
     Config
     List configs
     List projects
Output progress and stats
Add project config files and remove tie to directory name.
Auto cleanup of .yml files to quote or not.
Sorting
Add multiline description to use with things like c op precedence table
Localization
Installation notes:
    Need to separately install PyYAML.
Make links open in separate window.
Using id="{{ uid }}" for everything in templates could be a problem. First it
isn't obvious that the IDs are different. Second, if uid isn't defined in one
scope Mustache will look up the scope tree.
Don't include empty projects?
Make regex search options (and not default). It's annoying at times.
Unicode
Python 3
Ignore markdown in preformatted tags
