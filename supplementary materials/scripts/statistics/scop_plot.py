import matplotlib.pyplot as plt

# Data to plot
labels = 'All alpha', 'All beta', 'Alpha/beta', 'Alpha+beta', 'Multi-domain', 'Small proteins', 'Other'
sizes = [325,223,173,347,34,52,51]
# Plot
plt.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=140)

plt.axis('equal')
plt.savefig("scop.png")