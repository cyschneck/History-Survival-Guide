# python test_precession.py
import star_chart_spherical_projection

if __name__ == '__main__':
	star_chart_spherical_projection.plotStarPositionOverTime(builtInStarName="Vega",
							newStar=None,
							startYearSince2000=-15000,
							endYearSince2000=15000,
							isPrecessionIncluded=True,
							incrementYear=5,
							DecOrRA="D",
							showYearMarker=True,
							save_plot_name="test_precession_vondrak_example.png")
