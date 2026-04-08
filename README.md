# History Survival Guide
### A Time Traveler’s Guide to Surviving History

<picture>
  <source srcset="https://raw.githubusercontent.com/cyschneck/History-Survival-Guide/master/assets/Banner_Dark.jpg" media="(prefers-color-scheme: dark)">
  <img src="https://raw.githubusercontent.com/cyschneck/History-Survival-Guide/master/assets/Banner_Light.jpg">
</picture>

#### About This Project

The _**History Survival Guide**_ (or, A Time Traveler’s Guide to Surviving History) started in July 2019. History Survival Guide is pulp-era inspired STEM and history blog that explores  different engineer and scientific concepts with practical information about how to recreate by hand

Each page is the accumulation of research for a particular topic, synthesized, and summarized in a useful ‘survival guide’ format. So far, topics covered include using the proper motion of stars to determine what time period a time traveler could have found themselves in, deciphering over a hundred ‘Hobo Symbols’ of the 1800’s, how to read the Pioneer Plaque, and how to build an astrolabe by hand!

This github repo includes all relevant code and images used in a given guidebook page

[historysurvivalguide.com](http://historysurvivalguide.com/)

[Behind the Scenes - Tumblr](https://historysurvivalguide.tumblr.com/)

### [Proper Motion](https://github.com/cyschneck/History-Survival-Guide/tree/master/1_proper_motion)
Determine angular distance between two given stars

Included:
* Python code to determine the angular distance between two Stars

Guidebook page:

[Proper Motion](https://historysurvivalguide.com/determine-eon-proper-motion/)

### [Hobo Symbols](https://github.com/cyschneck/History-Survival-Guide/tree/master/2_hobo_symbols)
Hobo Signs and Symbols with definitions

Included:
* Each individual Hobo symbols (png) with 248 x 248 pixels dimensions (that is formatted for Slack)
* [Zip file with all symbols](https://github.com/cyschneck/History-Survival-Guide/blob/master/2_hobo_symbols/all_hobo_signs_and_symbols.zip)

| ![good_dog](https://github.com/cyschneck/History-Survival-Guide/blob/master/2_hobo_symbols/good_dog.png) | ![bad_dog](https://github.com/cyschneck/History-Survival-Guide/blob/master/2_hobo_symbols/bad_dog.png) |
| ------------- | ------------- |
| ![bad_man_with_gun](https://github.com/cyschneck/History-Survival-Guide/blob/master/2_hobo_symbols/bad_man_with_gun_lives_here.png) | ![kind_woman_lives_here](https://github.com/cyschneck/History-Survival-Guide/blob/master/2_hobo_symbols/kind_woman_lives_here.png) | ------------- | ------------- |
| ![safe_camp](https://github.com/cyschneck/History-Survival-Guide/blob/master/2_hobo_symbols/safe_camp.png) | ![courthouse](https://github.com/cyschneck/History-Survival-Guide/blob/master/2_hobo_symbols/courthouse.png) | | ------------- | ------------- |
 ![dangerous_drinking_water](https://github.com/cyschneck/History-Survival-Guide/blob/master/2_hobo_symbols/dangerous_drinking_water.png) | ![doctor](https://github.com/cyschneck/History-Survival-Guide/blob/master/2_hobo_symbols/doctor.png)

[Hobo Signs](https://historysurvivalguide.com/hobo-signs-and-symbols/)

### [Pioneer Plaque](https://github.com/cyschneck/History-Survival-Guide/tree/master/page_10_pioneer_plaque)

Clean PNG of the Pioneer Plaque

![pioneer_plaque+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/6_pioneer_plaque/full_scale_pioneer_plaque.png)

Reuse of this image is governed by [NASA's image use policy](https://www.nasa.gov/multimedia/guidelines/index.html).

 <p align="center">
  <img src="https://github.com/cyschneck/History-Survival-Guide/blob/master/6_pioneer_plaque/full_scale_diagram.jpg" width="50%" height="50%"/>
</p>

[Pioneer Plaque](https://historysurvivalguide.com/pioneer-plaque/)

### [Astrolabe](https://github.com/cyschneck/History-Survival-Guide/tree/master/12_astrolabe)

Currently uses: Python 3.12 (`pip install -r requirements.txt`)

**Constructing a Base Plate**

Base plate includes the position of the Tropic of Cancer, Tropic of Capricorn, and the Equator in three concentric circles. The position of each circle is due to the obliquity of the planet and over time the obliquity of Earth can shift

Corrected for obliquities between 0°-89.99° (undefined at 90°) when radius of base plate is 1

```python generate_base_plate.py```

```
outer_tropic_radius = base_plate_radius
equator_radius = base_plate_radius / (tan(45° + (obliquity / 2))
inner_tropic_radius = base_plate_radius / (tan(45° - (obliquity / 2))
```
![change_in_obliquity_radius+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/12_astrolabe/generate_base_plate_outputs/base_plate_change_due_to_obliquity.png)
![earth_base_plate+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/12_astrolabe/generate_base_plate_outputs/base_plate_for_earth_at_23.4_degrees.png)

Currently, uses [star-chart-spherical-projection package](https://github.com/cyschneck/Star-Chart-Spherical-Projection)

```
import star_chart_spherical_projection

star_chart_spherical_projection.plotStarPositionOverTime(builtInStarName="Vega",
							newStar=None,
							startYearSince2000=-15000,
							endYearSince2000=15000,
							isPrecessionIncluded=True,
							incrementYear=5,
							DecOrRA="D")
```
![test_prcession_star+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/12_astrolabe/test_precession_vondrak_example.png)

**Constructing Eccentric Calendar for Back Plate**

An eccentric calendar assumes the sun moves at a constant speed throughout the year but accounts for the Sun's true anomaly as an offset from the Vernal Equinox. Due to both *longitude* and the *year since 2000*, the center of the calendar will be placed at an offset from the center of the back plate of the astrolabe on the line of apsides (the line connecting the perihelion and aphelion)

Code will generate both the angular distance from the Vernal Equinox to the January 0 (midnight of December 31) at the beginning of the year as well as the offset (x, y) from the center of the back plate

```python calculate_eccentric_calendar_offset.py```

Variables:
1. Year to calculate (for example: 2026)
2. The longitude of the observer (-71.05° for Boston, -105.27° for Boulder, 0° for Greenwich, 13.74° for Dresden)
3. Radius of the back plate

```
For the Year 2026 at longitude -105.2705° for a plate with a radius of 1

T = 0.260000
Eccentricity = 0.016698
Offset of calendar center = 2e = 0.033395
Perihelion = 103.384456°
Aphelion   = 283.384456°

Morrison: Mean Anomaly of Jan 0 = 357.282167°
Meeus:    Mean Anomaly of Jan 0 = 357.282174°
Meeus     Mean Anomaly of Jan 0 = 357.280798°

Ecliptic longitude (λ) = -105.27049999999997
The angular distance from the vernal equinox to January 0 = π + M0 + λ / 365
(283.38445607308245° + 357.2807975051346° + 105.2705°) / 365
Line of Apside relative to Vernal Equinox = -78.63685738068705°

Offset due to Eccentricity with radius of 1 = 0.033395
X offset with radius of 1 = -0.007730
Y offset with radius of 1 = 0.032488
```
_How Eccentricity Changes over Time_
![change_in_year_eccentricity+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/12_astrolabe/calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_year_versus_eccentricity.png)
_How Offset (X, Y) Changes over Time_
![change_in_year_offset+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/12_astrolabe/calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_year_versus_offset.png)
_How Changing the Longitude Changes the Angular Distance to the Vernal Equinox_
![change_in_longitude_angular_distance+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/12_astrolabe/calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_longitude_versus_angular_distance.png)
_How Changing the Mean Anomaly Changes over Time_
![change_in_longitude_angular_distance+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/12_astrolabe/calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_time_vs_mean_anomaly.png)


