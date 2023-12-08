import asyncio
import pytz
from aiohttp import ClientSession
from metno import MetWeatherData  # Replace 'your_module' with the actual module name
import plotly.graph_objs as go
import plotly.io as pio

async def main():
    # Define your location's coordinates
    urlparams = {'lat': '61.98', 'lon': '7.33'}  # Example coordinates

    # Create an asynchronous web session and fetch weather data
    async with ClientSession() as session:
        met_weather_data = MetWeatherData(urlparams, websession=session)
        await met_weather_data.fetching_data()
        forecast_data = met_weather_data.get_forecast(pytz.timezone('Europe/Oslo'), hourly=True, range_start=1, range_stop=73)
        temperatures = [data_point['temperature'] for data_point in forecast_data]
        timestamps = [data_point['datetime'] for data_point in forecast_data]
        # Get current weather or forecast

        pio.renderers.default = "browser"  # Ensure plots open in the web browser

# Create a Plotly graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=timestamps, y=temperatures, mode='lines+markers', name='Temperature', line_shape='spline'))

        # Set plot layout
        fig.update_layout(title='Next 12 Hour Temperature Forecast',
                        xaxis_title='Time',
                        yaxis_title='Temperature (°C)',
                        xaxis=dict(
                            tickformat='%H:%M\n%d-%m'  # Format for hours and minutes
                        ))

        # Show the plot
        fig.show()
        # Add more processing as needed...

# Run the main coroutine
asyncio.run(main())