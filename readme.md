# Aeth Participation Bot
Aeth Participation bot is a custom event participation tracker for the Aetherial Senate [AETH] to allow event leaders to update the participation Google Sheet using Discord commands.

## Required Packages
### GSpread
#### Connects python with the Google Sheets API
```bash
pip install gspread
```

## Usage
### Connect to Google Sheet
```bash
!set_sheet Name_of_Sheet
```
Only needs to be done once, each time the bot is started.  The command checks the list of all Google Workbooks the bot has been authorized with and sets the active working sheet as the first sheet in the specified file.

###### Example
```bash
!set_sheet "Active Roster"
```

### Log Participation
```bash
!log Participation_Type 
Player_Name [Points_to_log]
```

Logs participation in the active working sheet.  Can accept an arbitrary number of lines containing lines of the above format (multilines in Discord are performed with Shift+Enter).  If no value is specified, the logged points defaults to 1.
Valid participation types are:
+ bonus
+ poobadoo
+ event

###### Example
```bash
!log poobadoo
player_1
player_2 2

>player_1 earns 1 points towards poobapacks
>player_2 earns 2 points towards poobapacks
```

#### Event participation
The number of times a member has led an event is tracked by including the option "--leader" flag to their input line.
###### Example
```bash
!log event
player_1 --leader
player_2

>player_1 earns 1 point towards events and 1 point towards leading
>player_2 earns 1 points towards events
```

### Discord.py
#### Python wrapper for the Discord API
```bash
pip install discord.py
```

## .env Required Information
\# todo