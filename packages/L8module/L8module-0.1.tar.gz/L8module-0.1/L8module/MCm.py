import random
import matplotlib.pyplot as plt

MCm = [ #Marcov Chain model: 0 = Bull, 1 = Bear, 2 = Recession
    [0.9, 0.075, 0.025],  
    [0.15, 0.8, 0.05],    
    [0.25, 0.25, 0.5]
]

def simulate_stock_market(num_days):
    state = random.randint(0, 2)
    stateCounts = [0, 0, 0] 
    for _ in range(num_days):
        stateCounts[state] += 1
        state = random.choices([0, 1, 2], weights=MCm[state])[0]
    total_days = sum(stateCounts)
    fractions = [count / total_days for count in stateCounts]
    return fractions

days = np.logspace(1,6,40)
trackFrac = np.zeros((len(days), 3))
for i, num_days in enumerate(days):
    fractions = simulate_stock_market(int(num_days))
    trackFrac[i] = fractions

# Plot the fractions over the days simulated
plt.figure(figsize=(10, 6))
plt.plot(days, trackFrac[:, 0], label='Bull')
plt.plot(days, trackFrac[:, 1], label='Bear')
plt.plot(days, trackFrac[:, 2], label='Recession')
plt.xscale('log')
plt.xlabel('Days')
plt.ylabel('Fraction of days')
plt.title('Fractions of days in each state over time')
plt.legend()
plt.grid(True)
plt.show()

