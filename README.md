 Tool for Evaluating Flight Performance

Aerodynamic file ingestion operations may be entirely automated using this lightweight, standalone desktop GUI program that was developed using Python, Tkinter, and Pandas.

Characteristics in order to upload and read external data sheets directly, it uses the normal OS file dialogue prompts.
The Performance Evaluation Engine uses vectorized Pandas DataFrame filtering to compute Lift-to-Drag aerodynamic efficiency and query data arrays.
When a Stall state (AoA ≥ 20°) is reached, a visual alert is triggered by the Closed-Loop Safety Track, which automatically verifies spatial parameters against physical boundaries.

Stack & Project ArchitectureEnvironment: Anaconda Navigator Deployment with Python 3.x
Two essential packages are Pandas (Data Ingestion Infrastructure) and Tkinter (User Interface Framework).
