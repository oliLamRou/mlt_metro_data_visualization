INTRO = """
# Analysis of STM and REM Lines  
In this analysis, we'll examine data from Twitter dating back to 2013 to compare interruptions on
the STM (Société de transport de Montréal) and REM (Réseau express métropolitain) lines.
Specifically, we aim to identify which line experiences more interruptions and whether there is a discernible pattern.  

**Source**: Data from twitter that goes back to 2013. *stm_BLEUE*, *stm_JAUNE*, *stm_ORANGE*, *stm_VERTE*, *REM_infoservice*
  
##### Analysis:
1. Compile the number of interruptions reported for each line.
2. Record the duration of each reported interruption.
3. Compile the number of interruptions for each station.

##### Potential Observations:
- The REM is a new, automated line with screen doors at each station, which may make it more reliable than the older STM system.
- Identify any seasonality in interruptions based on actual seasons or the pandemic.
- Determine if there are more problems downtown or around certain transfer stations.
"""

PER_YEAR = """
##### STM
- No surprise that the longest line have the most interruption.  
- There is an up trend that suggest a network getting older and/or more people can create incident.
- The pandemic was a down moment for the network and still there is more and more interuption
##### REM
- REM started in august 2023. So far with it's 5 station it perform roughly like the Bleue and Yellow line when looking at total amount and duration.
"""

PER_LINE = """
##### REM
- Looking at the REM, it had a rough start but very quickly is under average when looking at STM lines.
"""

ELEVATOR = """
##### STM
- Around 2016 the STM start to installed elevator. Prior to that none of there 68 station was equiped.
- We can see the evolution of that by looking at all mention of 'ascenseur'
##### REM
- The REM has elevator in each station from day 1. There was a lot of days where an elevator was broken. So far in 2024 there was no problem.
"""