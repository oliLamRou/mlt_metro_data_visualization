INTRO = """
# STM and REM Lines analysis
In this analysis, we'll examine data from Twitter dating back to 2013 to compare interruptions on the 
STM (Société de transport de Montréal) and REM (Réseau express métropolitain) lines. 
Specifically, we aim to identify which line experiences more interruptions and whether there is a discernible pattern.

**Source:** Data from Twitter dating back to 2013. 
Accounts include: *stm_BLEUE*, *stm_JAUNE*, *stm_ORANGE*, *stm_VERTE*, *REM_infoservice*.

##### Analysis:
1. Compile the number of interruptions reported for each line.
2. Record the duration of each reported interruption.
3. Compile the number of interruptions for each station.
4. Compile elevator interruptions too since it can reduce the accessibility.

##### Expected Observations:
- The REM is a new, automated line with screen doors at each station, which may make it more reliable than the older STM system.
- Identify any seasonality in interruptions based on actual seasons or the pandemic.
- Determine if there are more problems downtown or around certain interchange stations.
"""

PER_YEAR = """
##### STM
- Uptrend since 2013  
- A huge par of the population was working from home in 2020-2022. That didn't slow the uptrend.
##### REM
- Since the REM is an automated train they had many interruption du to the system problem.  
i.e. date: tweet...  
- Without a full year yet it's hard to 
- REM started in august 2023. So far with it's 5 station it perform roughly like the Bleue and Yellow line when looking at total amount and duration.
"""

PER_LINE = """
##### REM
- Looking at the REM, it had a rough start but very quickly is under average when looking at STM lines.
"""

PER_STATION = """
##### STM  
- Lionel-Groulx and Berri-UQAM are interchange station and they have a higher rate of interruption.
- Snowdon and Jean-Talon are also interchange station but it doesn't seem to have an impact.
- On the Bleue line it's Parc station that getting shotdown the most.
##### REM
- For now the line seems to be fully open or close. Will be interresting to see when the network is completed.  
"""

ELEVATOR = """
##### STM
- Around 2016 the STM start to installed elevator. Prior to that none of there 68 station was equiped.
- We can see the evolution of that by looking at all mention of 'ascenseur'
##### REM
- The REM has elevator in each station from day 1. There was a lot of days where an elevator was broken. So far in 2024 there was no problem.
"""

CONCLUSION = """
### Conclusion
It's too early to really compare 
"""