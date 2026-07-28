## Changes from upstream

### Purpose:
- Allow easier maintenance to existing API/dictionary providers and add new ones

### Added
- providers/sqlite_2_provider.py which is a sqlite3 database built from wordnet
using [github ishaanrajiv/SQLite-Offline-Dictionary](https://github.com/ishaanrajiv/SQLite-Offline-Dictionary/blob/main/README.md). This is the only active and tested provider. 

### Changed
- changed general program flow to allow for easier provider updates. Providers are where the data/dictionary comes from. They can be databases, APIs, JSON, etc.
- To add a new provider: define it in providers and update build_serivce (rofi_dictionary.py) function to use it. 

### Removed
- removed Oxford api embended code from rofi_dictionary.py and api_requester.py. it's planned to be added back, but i have work todo.
- remove api_requester.py, no longer used, rework flow of program.

### Todo
- add and test Oxford api
- add wiktionary api
- cleanup providers/
- re-implement config.json where items have been hard coded. 

