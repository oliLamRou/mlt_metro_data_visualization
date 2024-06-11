INTRO = """
# Montreal metro network analysis
##### For STM(Société de transport de Montréal) & REM(Réseau express métropolitain)
In this analysis, we will examine service interruptions by line and station, as well as assess elevator accessibility.
**Source:** Data from Twitter dating back to 2013. 
Accounts include: *stm_BLEUE*, *stm_JAUNE*, *stm_ORANGE*, *stm_VERTE*, *REM_infoservice*.

##### Analysis:
1. Compile the number of service interruptions reported for each line.
2. Record the duration of each reported interruption.
3. Compile the number of interruptions for each station.
4. Compile elevator mentions and interruptions since it can also reduce the accessibility.

##### Expected Observations:
- The REM is a new, automated line with screen doors at each station, which may make it more reliable than the older STM system.
- Identify any seasonality in interruptions based on actual seasons or the pandemic.
- Determine if there are more problems in any section of the network like downtown or around certain interchange stations.
"""

PER_YEAR = """
##### STM
- Uptrend since 2013  
- A huge par of the population was working from home in 2020-2022. That didn't slow the uptrend.
##### REM
- REM started in august 2023. So far with it's 5 station it perform roughly like the Bleue and Yellow line when looking at total amount and duration.
- Since the REM is an automated train they had many interruption du to the system problem.  
For example: **2024-03-02 13:25:25 Interruption  –  Une panne de système de contrôle cause une interruption de service sur le réseau...**
- With more time it will be interresting to see if they can make the system more robust.
"""

PER_LINE = """
##### STM
- Interruptions happen often, but are generally short.  
- There are various reasons for these interruptions, including both external factors and issues with the train itself.  
For example: **Arrêt ligne ORANGE entre Berri-UQAM et Montmorency. Dégagement de fumée...** or **Arrêt ligne ORANGE entre Côte-Vertu et L-Groulx. Panne de train...**
##### REM
- Looking at the REM (5 stations), it has a similar pattern to stm_jaune (3 stations). They both cross the St-Laurent 
river and have a key role in serving south shore commuters.
- It's still too early to tell how much better this system is.
"""

PER_STATION = """
##### STM  
- Lionel-Groulx and Berri-UQAM, as interchange stations, have a higher rate of interruptions.
- Snowdon and Jean-Talon are also interchange stations, but this doesn't seem to have an impact on their interruption rates.
- On the Bleue line, Parc station is particularly prone to service disruptions.
##### REM
- For now, the line seems to be fully open or closed. It will be interesting to see when the network is completed with 
over 20 more stations.
"""

ELEVATOR = """
##### STM
- Around 2016, the STM started installing elevators. Prior to that, none of their 68 stations were equipped.
- We can see the evolution of this by looking at all mentions of 'ascenseur'.
- Assuming there is good reporting on elevator service, it appears to be reliable.
##### REM
- The REM has had elevators in each station from day one. Initially, there were some days where an elevator was broken. However, as of 2024, we have not seen any issues.
##### ARTM
- Please note that the infrastructure, including elevators and ticket machines, is managed by the ARTM (Autorité régionale de transport métropolitain).
"""

CONCLUSION = """
### Conclusion
##### STM
The stm_bleue line is set to be extended eastward in the coming years. The STM is also in the process of decommissioning older trains for new ones.
##### REM
It's too early to make meaningful comparisons between both networks. The REM, with its automated system and screen doors, needs to demonstrate its reliability. In 2025, two new lines with 18 new stations will open. Additionally, in 2027, two more stations will come online, including one at the YUL airport.
  
Let's see how the network evolves in a couple of years. Thank you for taking the time to read my data science final project.
"""