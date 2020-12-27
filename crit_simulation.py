Attacks_per_Second = 1.36
BASE_Critical_Hit_Chance = 29.5
Critical_Hit_Damage = 305
SS_DPS = 87048.78



num_simulations = 4000
shots_in_simulation = 25





import math
import sys
import random
from subprocess import Popen, PIPE

def get_crit_dps( dps, chance, bonus ):
    return ( dps * ( chance * bonus + ( 1.0 - chance ) ) )

def string_percent( chance, precision = 0 ):
    return '{0:.2f}%'.format( round( chance * 100, precision ) )

aps = Attacks_per_Second
base_crit_chance = BASE_Critical_Hit_Chance / 100.0
crit_bonus = 1.0 + Critical_Hit_Damage / 100.0


print '\nAttacks per Second:                         {0:.2f}'.format( aps )
print 'Critical Hit Chance (without Sharpshooter): {0}'.format( string_percent( base_crit_chance ) )
print 'Critical Hit Damage:                        {0}'.format( string_percent( crit_bonus - 1.0 ) )
print 'DPS with crit:                              {0}'.format( SS_DPS )

random.seed()

crit_chance = base_crit_chance
is_sharpshooter_enabled = True
if is_sharpshooter_enabled:
    crit_chance = 1.0
delta_crit = 0.03

crits = []

for s in range( num_simulations ):
    #simulation
   
    crits_in_simulation = 0
    global_second = 0
    last_global_second = 0

    was_crit = False
    crit_second = 0
    second_from_crit = 0

    for i in range( shots_in_simulation ):
        #shot

        if is_sharpshooter_enabled:
            last_global_second = global_second
            global_second = i / aps
            if math.floor( global_second ) > math.floor( last_global_second ):
                if last_global_second == crit_second:
                    crit_chance = base_crit_chance
                crit_chance = min( crit_chance + delta_crit, 1.0 )

        if random.random() <= crit_chance:
            crits_in_simulation += 1
            if is_sharpshooter_enabled:
                crit_second = global_second
               
    crits += [crits_in_simulation]

print '\n\nSharpshooter bonus:\n'

average_crit_chanse = 1.0 * sum( crits ) / ( len( crits ) * shots_in_simulation )
crit_profit = average_crit_chanse - base_crit_chance
print 'Crit chanse: {0}\t-> {1}\t(+{2})'.format( string_percent( base_crit_chance, 2 ), string_percent( average_crit_chanse, 2 ), string_percent( crit_profit, 2 ), )

crit_dps = SS_DPS

nocrit_dps = SS_DPS / crit_bonus
base_dps = get_crit_dps( nocrit_dps, base_crit_chance, crit_bonus )
average_dps = get_crit_dps( nocrit_dps, average_crit_chanse, crit_bonus )
dps_profit = ( average_dps / base_dps - 1.0 )

print 'DPS:         {0:.2f}\t-> {1:.2f}\t(+{2})'.format( base_dps, average_dps, string_percent( dps_profit, 2 ) )

sys.stdin.read( 1 )