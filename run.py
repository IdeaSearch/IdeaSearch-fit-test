import numpy as np
from IdeaSearch import IdeaSearcher
from IdeaSearch_fit import IdeaSearchFitter


def build_data():
    
    n_samples = 1000
    rng = np.random.default_rng(seed=42)

    A_range = (1.0, 10.0)
    gamma_range = (0.1, 1.0)
    omega_range = (1.0, 5.0)
    t_range = (0.0, 10.0)

    A_samples = rng.uniform(A_range[0], A_range[1], n_samples)
    gamma_samples = rng.uniform(gamma_range[0], gamma_range[1], n_samples)
    omega_samples = rng.uniform(omega_range[0], omega_range[1], n_samples)
    t_samples = rng.uniform(t_range[0], t_range[1], n_samples)

    x_data = np.stack([A_samples, gamma_samples, omega_samples, t_samples], axis=1)

    y_true = (1.2 * A_samples +
              A_samples * np.exp(-0.7 * gamma_samples * t_samples) -
              A_samples * np.exp(-0.5 * gamma_samples * t_samples) * np.cos(3 * omega_samples * t_samples))
    error_data = 0.01 + 0.02 * np.abs(y_true)
    y_data = y_true + rng.normal(0, error_data)
    return {
        "x": x_data,
        "y": y_data,
    }
    

def main():

    data = build_data()
    
    fitter = IdeaSearchFitter(
        result_path = "fit_results", # Ensure this directory exists
        data = data,
        variable_names = ["A", "gamma", "omega", "t"],
        variable_units = ["m", "s^-1", "s^-1", "s"],
        output_name = "x",
        output_unit = "m",
        constant_whitelist = ["1", "2", "pi"],
        constant_map = {"1": 1, "2": 2, "pi": np.pi},
        auto_polish = True,
        generate_fuzzy = True,
        perform_unit_validation = True,
        optimization_method = "L-BFGS-B",
        optimization_trial_num=5, 
    )

    ideasearcher = IdeaSearcher()

    ideasearcher.set_program_name("IdeaSearch Fitter Test")
    ideasearcher.set_database_path("database") # Ensure this directory exists
    ideasearcher.set_api_keys_path("api_keys.json")
    ideasearcher.set_models(["gemini-2.5-pro"]) # Use your desired model
    
    ideasearcher.set_record_prompt_in_diary(True) # optional

    ideasearcher.bind_helper(fitter)
    
    island_num = 3
    cycle_num = 3
    unit_interaction_num = 20

    for _ in range(island_num):
        ideasearcher.add_island()

    for cycle in range(cycle_num):
        print(f"---[ Cycle {cycle + 1}/{cycle_num} ]---")
        if cycle != 0: ideasearcher.repopulate_islands()
        ideasearcher.run(unit_interaction_num)
        print("Done.")

    print("\n---[ Search Complete ]---")
    print(f"Best Fit Formula: {fitter.get_best_fit()}")

    print("\nOptimal Solutions on the Pareto Frontier:")
    pareto_frontier = fitter.get_pareto_frontier()
    if not pareto_frontier:
        print("  - No solutions found on the Pareto frontier.")
    else:
        for complexity, info in sorted(pareto_frontier.items()):
            metric_key = "reduced chi squared" if "reduced chi squared" in info else "mean square error"
            metric_value = info.get(metric_key, float('nan'))
            print(f"  - Complexity: {complexity}, Error: {metric_value:.4g}, Formula: {info.get('ansatz', 'N/A')}")


if __name__ == "__main__":

    main()