"""Small, explainable forecasting primitives for sandbox execution."""

from statistics import mean

from .models import ForecastResult


def forecast_linear(metric_name: str, values: list[float], horizon: int = 4) -> ForecastResult:
    """Forecast using a least-squares trend with a simple uncertainty band."""
    if len(values) < 3:
        raise ValueError("At least three historical values are required")
    x_mean = (len(values) - 1) / 2
    y_mean = mean(values)
    denominator = sum((index - x_mean) ** 2 for index in range(len(values)))
    slope = sum((index - x_mean) * (value - y_mean) for index, value in enumerate(values)) / denominator
    intercept = y_mean - slope * x_mean
    residuals = [value - (intercept + slope * index) for index, value in enumerate(values)]
    spread = max(1.0, (sum(residual * residual for residual in residuals) / len(residuals)) ** 0.5)
    prediction = [max(0.0, intercept + slope * (len(values) + step)) for step in range(horizon)]
    baseline = [values[-1]] * horizon
    return ForecastResult(
        metric_name=metric_name,
        horizon=f"next {horizon} periods",
        baseline=baseline,
        prediction=prediction,
        lower_bound=[max(0.0, value - 1.96 * spread) for value in prediction],
        upper_bound=[value + 1.96 * spread for value in prediction],
        limitations=["Trend projection assumes recent patterns continue", "This is not a causal forecast"],
    )
