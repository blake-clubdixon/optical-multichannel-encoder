import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

n_0 = 1             #refractive index of air
n_1 = 1.49         #refractive index of PMMA
num_aperture = 0.5

long_gap = 0.001

fresnel_ref = ((n_1 - n_0)/(n_1 + n_0))**2
total_tran = (1-fresnel_ref)**2
fresnel_loss = -10*math.log10(total_tran) #light loss over coupling due to fresnel refraction

print("Fresnel Refraction Loss: ", fresnel_loss)

half_angle = math.degrees(math.asin(num_aperture))

print("Incident Half Angle: ", half_angle)

r = 0.001
delta_r = long_gap * math.tan(math.radians(half_angle))
r_z = r + delta_r
p_capture = (r/r_z)**2

print("Power Capture Ratio: ", p_capture)

gap_loss = -10 * math.log10(p_capture)          #light loss over air gap
P_emitter_loss = 0.000194                       #light loss from emitter to first fiber


P_diode = 0.005
P_in = P_diode - P_emitter_loss
P_out = 0.0
P_total = 0.0

coupling_loss = fresnel_loss + gap_loss

print("Coupling Loss: ", coupling_loss)

n_couplings = 10
j = 10**(-coupling_loss/10)

Power_data = {'Coupling': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'Remaining Power' : [(P_in)*(10**6)]}

for n in range(n_couplings):
    P_out = P_in * j
    Power_data['Remaining Power'].append((P_out)*(10**6))
    P_in = P_out

Power_data['Coupling'].append(11)       #accounts for power loss from fiber end to photodiode
Power_data['Remaining Power'].append(0.2213)

print("Total Power Remaining: ", P_out)



print(Power_data)

df = pd.DataFrame(Power_data)

fig, (ax1, ax2) = plt.subplots(1,2, figsize = (12, 5))

sns.lineplot(data=df, x='Coupling', y='Remaining Power', marker='o', color='blue', ax=ax1)
ax1.set_title('Optical Power Decay Across Couplings')
ax1.set_xlabel('Coupling')
ax1.set_ylabel('Remaining Power (uW)')
ax1.grid(True)

sns.lineplot(data=df, x='Coupling', y='Remaining Power', marker='o', color='red', ax=ax2)
ax2.set_yscale('log')
ax2.set_title('Optical Power Decay Across Couplings (log_10)')
ax2.set_xlabel('Coupling')
ax2.set_ylabel('Remaining Power (uW)')
ax2.grid(True, which='both', ls="--")


plt.tight_layout()
plt.show()