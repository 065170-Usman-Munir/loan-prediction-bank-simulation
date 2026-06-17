# Viva Questions & Answers

Prepared answers covering the ML, simulation, and software-engineering aspects of the project.

---

## A. General / Project Design

**Q1. What is your project about?**
It combines two banking problems: predicting loan approval with machine learning, and simulating customer queues at a bank branch using discrete-event simulation. Both are presented in one interactive Streamlit dashboard.

**Q2. Why combine prediction and simulation?**
They reflect the two halves of a Simulation & Modeling course — statistical learning and stochastic process modeling. They also connect operationally: faster automated loan decisions reduce service time, which the queue simulation can then use to re-optimize staffing.

**Q3. What is the difference between modeling and simulation?**
A *model* is a simplified mathematical representation of a system (e.g., the M/M/c equations). *Simulation* is running that model over time — often with randomness — to observe behaviour that may be hard to solve analytically.

---

## B. Dataset & EDA

**Q4. Describe your dataset.**
614 loan applications with 13 attributes: demographics, income, loan terms, credit history, property area, and the target `Loan_Status`. About 74% are approved.

**Q5. How did you handle missing values?**
Categorical columns were filled with the **mode**, numeric columns with the **median** (median resists outliers better than the mean).

**Q6. Why log-transform income and loan amount?**
Both are heavily right-skewed with a long tail. A log transform compresses the tail, reduces outlier leverage, and helps models train more stably.

**Q7. Which feature is most important?**
**Credit history** — the EDA heatmap and bar charts show it has by far the strongest relationship with approval.

**Q8. What features did you engineer?**
Total household income (applicant + co-applicant), log-loan amount, and an income-to-loan ratio.

---

## C. Machine Learning

**Q9. Which three models did you use and why?**
Logistic Regression (interpretable linear baseline), Decision Tree (simple non-linear rules), and Random Forest (an ensemble that reduces variance).

**Q10. How did you evaluate the models?**
Accuracy, Precision, Recall, F1 score, confusion matrix, and ROC-AUC, on an 80/20 stratified train-test split.

**Q11. Why did Logistic Regression perform best here?**
The dominant predictor (credit history) relates to approval almost linearly, so a linear boundary captures most of the signal. On a small 614-row dataset, the tree models slightly overfit the noisier engineered features. Logistic Regression is also the most interpretable, which matters for auditable lending.

**Q12. What is the difference between precision and recall?**
Precision = of those predicted approved, how many truly were (TP / (TP+FP)). Recall = of those truly approved, how many we caught (TP / (TP+FN)). F1 is their harmonic mean.

**Q13. Why scale features only for Logistic Regression?**
Logistic Regression is distance/gradient sensitive, so standardized features help convergence. Tree-based models split on thresholds and are scale-invariant, so scaling isn't needed.

**Q14. What is overfitting and how did you reduce it?**
When a model memorizes training noise and generalizes poorly. I limited tree depth (`max_depth`), used an ensemble (Random Forest), and evaluated on a held-out test set.

**Q15. What is a confusion matrix?**
A 2×2 table of True Positives, True Negatives, False Positives and False Negatives that shows exactly where the model is right and wrong.

**Q16. What does ROC-AUC measure?**
The ROC curve plots true-positive rate vs false-positive rate across thresholds; AUC is the area under it. 1.0 is perfect, 0.5 is random.

---

## D. Simulation

**Q17. What queueing model did you use?**
The **M/M/c** model: Markovian (Poisson) arrivals, Markovian (exponential) service times, and *c* parallel servers (tellers) sharing one FIFO queue.

**Q18. What do λ, μ, and ρ mean?**
λ = mean arrival rate, μ = mean service rate per teller, ρ = utilization = λ / (c·μ). The system is stable only when ρ < 1.

**Q19. Why exponential distributions?**
Exponential inter-arrival and service times are memoryless, which is the standard assumption for the M/M/c model and realistic for many service systems.

**Q20. What is Little's Law?**
L = λ·W — the average number in the system equals arrival rate times average time in the system. For the queue, Wq = Lq / λ.

**Q21. What is SimPy and how does it work?**
SimPy is a process-based discrete-event simulation library. Processes are Python generators that `yield` events (timeouts, resource requests); SimPy advances simulation time event-by-event rather than tick-by-tick.

**Q22. How is a teller represented?**
As a `simpy.Resource` with capacity = number of tellers. Customers `request()` it; if all are busy they wait in the queue automatically.

**Q23. What does the utilization graph tell you?**
Adding tellers lowers each teller's utilization but reduces waiting time. One or two tellers are overworked (long queues); five sit idle. Three tellers balance both for this arrival rate.

**Q24. Why simulate instead of using the formula?**
Closed-form Erlang-C formulas assume steady state. Simulation handles transient behaviour, bursts, and easy extension to non-standard arrival patterns.

---

## E. Software / Tools

**Q25. What is Streamlit?**
A Python framework for building interactive data web apps quickly, with no front-end code. Each widget interaction re-runs the script.

**Q26. Why save models as .pkl files?**
Pickling (via joblib) serializes the trained model to disk so the dashboard can load it instantly without retraining.

**Q27. What does `@st.cache_data` / `@st.cache_resource` do?**
They cache expensive operations (loading data or models) so they aren't recomputed on every interaction, keeping the app responsive.

**Q28. How would you improve this project?**
Add gradient-boosting (XGBoost) with hyperparameter tuning, use time-varying arrival rates for rush hours, add priority queues, and deploy the dashboard to the cloud with a live database.

**Q29. What libraries did you use?**
Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn, SimPy, and Streamlit.

**Q30. Is your dataset real?**
It follows the exact schema and distribution of the public Kaggle Loan Prediction dataset; a reproducible version is bundled so the project runs without a Kaggle login. The original source is linked in the README.
