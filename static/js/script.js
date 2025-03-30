document.addEventListener("DOMContentLoaded", function () {
  // Tab switching
  const tabButtons = document.querySelectorAll(".tab-button");
  const tabContents = document.querySelectorAll(".tab-content");

  // Form elements
  const ageInput = document.getElementById("age");
  const genderSelect = document.getElementById("gender");
  const weightInput = document.getElementById("weight");
  const heightInput = document.getElementById("height");
  const bmiInput = document.getElementById("bmi");
  const activityLevelSelect = document.getElementById("activity-level");
  const goalSelect = document.getElementById("goal");
  const vegetarianCheckbox = document.getElementById("vegetarian");
  const veganCheckbox = document.getElementById("vegan");
  const lowCarbCheckbox = document.getElementById("low-carb");
  const lowFatCheckbox = document.getElementById("low-fat");
  const highProteinCheckbox = document.getElementById("high-protein");
  const allergiesInput = document.getElementById("allergies");

  // Buttons
  const calculateBmiButton = document.getElementById("calculate-bmi");
  const generateRecommendationsButton = document.getElementById(
    "generate-recommendations"
  );
  const viewVisualizationButton = document.getElementById("view-visualization");

  // Weekly meal plan elements
  const weeklyTabButtons = document.querySelectorAll(
    ".weekly-tab-content button"
  );
  const weeklyDietTable = document.querySelector(".weekly-diet-table");

  // Loading and error elements
  const loadingOverlay = document.getElementById("loading-overlay");
  const errorModal = document.getElementById("error-modal");
  const errorMessage = document.getElementById("error-message");
  const closeButton = document.querySelector(".close-button");

  // Chart objects
  let macrosChart = null;
  let dailyCaloriesChart = null;
  let nutrientComparisonChart = null;
  let mealDistributionChart = null;

  // Current active day for meal plan
  let currentActiveDay = "";

  // Set up event listeners
  setupEventListeners();

  // Initialize
  function setupEventListeners() {
    // Tab switching
    tabButtons.forEach((button) => {
      button.addEventListener("click", () => switchTab(button.dataset.tab));
    });

    // BMI calculation
    calculateBmiButton.addEventListener("click", calculateBMI);

    // Auto calculate BMI when weight and height are entered
    weightInput.addEventListener("change", calculateBMI);
    heightInput.addEventListener("change", calculateBMI);

    // Generate recommendations
    generateRecommendationsButton.addEventListener(
      "click",
      generateRecommendations
    );

    // View visualization
    viewVisualizationButton.addEventListener("click", () =>
      switchTab("visualization")
    );

    // Vegetarian/Vegan dependency
    veganCheckbox.addEventListener("change", function () {
      if (this.checked) {
        vegetarianCheckbox.checked = true;
      }
    });

    vegetarianCheckbox.addEventListener("change", function () {
      if (!this.checked) {
        veganCheckbox.checked = false;
      }
    });

    // Close error modal
    closeButton.addEventListener(
      "click",
      () => (errorModal.style.display = "none")
    );
    window.addEventListener("click", (e) => {
      if (e.target === errorModal) {
        errorModal.style.display = "none";
      }
    });
  }

  // Switch between tabs
  function switchTab(tabId) {
    // Update button active states
    tabButtons.forEach((button) => {
      button.classList.toggle("active", button.dataset.tab === tabId);
    });

    // Show selected tab content
    tabContents.forEach((content) => {
      content.classList.toggle("active", content.id === tabId);
    });

    // Initialize charts when visualization tab is selected
    if (tabId === "visualization") {
      fetchVisualizationData();
    }
  }

  // Calculate BMI
  function calculateBMI() {
    const weight = parseFloat(weightInput.value);
    const height = parseFloat(heightInput.value);

    if (weight > 0 && height > 0) {
      fetch("/calculate_bmi", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ weight, height }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            showError(data.error);
          } else {
            bmiInput.value = data.bmi;

            // Add BMI category text
            let bmiCategory = "";
            if (data.bmi < 18.5) {
              bmiCategory = " (Underweight)";
            } else if (data.bmi < 25) {
              bmiCategory = " (Normal)";
            } else if (data.bmi < 30) {
              bmiCategory = " (Overweight)";
            } else {
              bmiCategory = " (Obese)";
            }

            bmiInput.value = `${data.bmi}${bmiCategory}`;
          }
        })
        .catch((error) => {
          showError("Failed to calculate BMI: " + error);
        });
    }
  }

  // Generate diet recommendations
  function generateRecommendations() {
    // Validate required fields
    if (!validateForm()) {
      return;
    }

    // Show loading overlay
    loadingOverlay.style.display = "flex";

    // Collect form data
    const formData = {
      age: parseInt(ageInput.value),
      gender: genderSelect.value,
      weight: parseFloat(weightInput.value),
      height: parseFloat(heightInput.value),
      activity_level: activityLevelSelect.value,
      goal: goalSelect.value,
      vegetarian: vegetarianCheckbox.checked,
      vegan: veganCheckbox.checked,
      low_carb: lowCarbCheckbox.checked,
      low_fat: lowFatCheckbox.checked,
      high_protein: highProteinCheckbox.checked,
      allergies: allergiesInput.value,
    };

    // Send request to API - updated endpoint name
    fetch("/generate_weekly_plan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        loadingOverlay.style.display = "none";

        if (data.error) {
          showError(data.error);
        } else {
          displayRecommendations(data);
          switchTab("recommendations");
        }
      })
      .catch((error) => {
        loadingOverlay.style.display = "none";
        showError("Failed to generate recommendations: " + error);
      });
  }

  // Validate form inputs
  function validateForm() {
    if (!ageInput.value || ageInput.value <= 0) {
      showError("Please enter a valid age.");
      return false;
    }

    if (!weightInput.value || weightInput.value <= 0) {
      showError("Please enter a valid weight.");
      return false;
    }

    if (!heightInput.value || heightInput.value <= 0) {
      showError("Please enter a valid height.");
      return false;
    }

    return true;
  }

  // Display recommendations
  function displayRecommendations(data) {
    // Display nutrition requirements
    const averageDailyNutritionReq = data.nutritional_totals.daily_average;
    document.getElementById("nutrition-requirements").innerHTML = `
          <p><strong>Daily Calories:</strong> ${averageDailyNutritionReq.calories} kcal</p>
          <p><strong>Protein:</strong> ${averageDailyNutritionReq.protein}g</p>
          <p><strong>Carbohydrates:</strong> ${averageDailyNutritionReq.carbs}g</p>
          <p><strong>Fat:</strong> ${averageDailyNutritionReq.fat}g</p>
          <p><strong>Fiber:</strong> ${averageDailyNutritionReq.fiber}g</p>
        `;

    const weeklyNutritionReq = data.nutritional_totals.weekly;
    document.getElementById("nutrition-requirements-weekly").innerHTML = `
          <p><strong>Daily Calories:</strong> ${weeklyNutritionReq.calories} kcal</p>
          <p><strong>Protein:</strong> ${weeklyNutritionReq.protein}g</p>
          <p><strong>Carbohydrates:</strong> ${weeklyNutritionReq.carbs}g</p>
          <p><strong>Fat:</strong> ${weeklyNutritionReq.fat}g</p>
          <p><strong>Fiber:</strong> ${weeklyNutritionReq.fiber}g</p>
        `;

    const firstDay = weeklyTabButtons[0];
    firstDay.classList.add("active");

    weeklyTabButtons.forEach((button) => {
      button.addEventListener("click", (evtObj) => {
        weeklyTabButtons.forEach((button) => {
          button.classList.remove("active");
        });
        button.classList.add("active");
        displayDayMealPlan(data.weekly_plan[button.innerHTML]);
      });
    });

    weeklyTabButtons.forEach((button) => {
      button.classList.contains("active") &&
        displayDayMealPlan(data.weekly_plan[button.innerHTML]);
    });
  }

  // Display meal plan for a specific day in the table
  function displayDayMealPlan(dayPlan) {
    console.log(dayPlan);
    const breakfastFoodBox1 = document.querySelector(".breakfastFood1");
    breakfastFoodBox1.innerHTML = `${dayPlan.breakfast[0].Food_items}`;
    const breakfastFoodBox2 = document.querySelector(".breakfastFood2");
    breakfastFoodBox2.innerHTML = `${dayPlan.breakfast[1].Food_items}`;

    const lunchFood1 = document.querySelector(".lunchFood1");
    lunchFood1.innerHTML = `<span>${dayPlan.lunch[0].Food_items}</span>`;
    const lunchFood2 = document.querySelector(".lunchFood2");
    lunchFood2.innerHTML = `<span>${dayPlan.lunch[1].Food_items}</span>`;

    const snackFood1 = document.querySelector(".snackFood1");
    snackFood1.innerHTML = `<span>${dayPlan.snacks[0].Food_items}</span>`;
    const snackFood2 = document.querySelector(".snackFood2");
    snackFood2.innerHTML = `<span>${dayPlan.snacks[1].Food_items}</span>`;

    const dinnerFood1 = document.querySelector(".dinnerFood1");
    dinnerFood1.innerHTML = `<span>${dayPlan.dinner[0].Food_items}</span>`;
    const dinnerFood2 = document.querySelector(".dinnerFood2");
    dinnerFood2.innerHTML = `<span>${dayPlan.dinner[1].Food_items}</span>`;
  }

  // Fetch data for visualizations
  function fetchVisualizationData() {
    fetch("/get_visualizations_data")
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          showError(data.error);
        } else {
          createVisualizationCharts(data);
        }
      })
      .catch((error) => {
        showError("Failed to load visualization data: " + error);
      });
  }

  // Create visualization charts
  function createVisualizationCharts(data) {
    // Destroy existing charts to prevent duplicates
    if (macrosChart) macrosChart.destroy();
    if (dailyCaloriesChart) dailyCaloriesChart.destroy();
    if (nutrientComparisonChart) nutrientComparisonChart.destroy();

    // Create macronutrient breakdown chart (pie chart)
    const macrosCtx = document.getElementById("macros-chart").getContext("2d");
    macrosChart = new Chart(macrosCtx, {
      type: "pie",
      data: {
        labels: data.macros.labels,
        datasets: [
          {
            data: data.macros.values,
            backgroundColor: [
              "#4CAF50", // Protein - green
              "#FF9800", // Carbs - orange
              "#2196F3", // Fat - blue
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = Math.round((context.raw / total) * 100);
                return `${context.label}: ${percentage}%`;
              },
            },
          },
        },
      },
    });

    // Create meal calories chart (bar chart)
    const mealCaloriesCtx = document
      .getElementById("meal-calories-chart")
      .getContext("2d");
    dailyCaloriesChart = new Chart(mealCaloriesCtx, {
      type: "bar",
      data: {
        labels: data.meal_calories.labels,
        datasets: [
          {
            label: "Calories by Meal",
            data: data.meal_calories.values,
            backgroundColor: [
              "#4CAF50", // Breakfast - green
              "#2196F3", // Lunch - blue
              "#FF9800", // Dinner - orange
              "#9C27B0", // Snacks - purple
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: "Calories (kcal)",
            },
          },
        },
      },
    });

    // Create nutrient comparison chart (bar chart)
    const nutrientComparisonCtx = document
      .getElementById("nutrient-comparison-chart")
      .getContext("2d");
    nutrientComparisonChart = new Chart(nutrientComparisonCtx, {
      type: "bar",
      data: {
        labels: data.nutrient_comparison.nutrients,
        datasets: [
          {
            label: "Recommended",
            data: data.nutrient_comparison.recommended,
            backgroundColor: "#81C784",
            borderColor: "#4CAF50",
            borderWidth: 1,
          },
          {
            label: "Actual in Meal Plan",
            data: data.nutrient_comparison.actual,
            backgroundColor: "#FF9800",
            borderColor: "#F57C00",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: "Amount (g)",
            },
          },
        },
      },
    });
  }

  // Show error modal
  function showError(message) {
    errorMessage.textContent = message;
    errorModal.style.display = "block";
  }
});
