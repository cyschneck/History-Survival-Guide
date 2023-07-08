# History Survival Guide
### A Time Traveler’s Guide to Surviving History

<picture>
  <source srcset="https://raw.githubusercontent.com/cyschneck/History-Survival-Guide/master/assets/Banner_Dark.jpg" media="(prefers-color-scheme: dark)">
  <img src="https://raw.githubusercontent.com/cyschneck/History-Survival-Guide/master/assets/Banner_Light.jpg">
</picture>

**About This Project**

This is a science and history blog that explores scientific concepts coupled with practical information about how to recreate and use the techniques described by hand.  The History Survival Guide (or,  A Time Traveler’s Guide to Surviving History) has been updating since July 2019. Each page is the accumulation of research for a particular topic, synthesized and summarized in a useful ‘survival guide’ format. So far, topics covered included using the proper motion of stars to determine what time period a time traveler could have found themselves in, deciphering ‘Hobo Symbols’ from the 1800’s, reading the Pioneer Plaque, and constructing an astrolabe from scratch. All pages are done in a pulp science fiction aesthetic.

This github repo includes all relevant code and images used in a given guidebook page for public use

[historysurvivalguide.com](http://historysurvivalguide.com/)

[Behind the Scenes - Tumblr](https://historysurvivalguide.tumblr.com/)

[3D Models - Printables](https://www.printables.com/social/328713-cyschneck/about)


### [Page 1: Proper Motion](https://github.com/cyschneck/History-Survival-Guide/tree/master/page_1_proper_motion)
Determine angular distance between two given stars

Included:
* Python code to determine the angular distance between two Stars

Guidebook page:

[Page 1: Proper Motion](http://historysurvivalguide.com/page/determine-eon-proper-motion/)

### [Page 3-6: Hobo Symbols](https://github.com/cyschneck/History-Survival-Guide/tree/master/page_3_hobo_symbols)
Hobo Signs and Symbols with definitions

Included:
* Each individual Hobo symbols (png) with 248 x 248 pixels dimensions (that is formatted for Slack)
* [Zip file with all symbols](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_3_hobo_symbols/all_hobo_signs_and_symbols.zip)

| ![good_dog](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_3_hobo_symbols/good_dog.png) | ![bad_dog](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_3_hobo_symbols/bad_dog.png) |
| ------------- | ------------- |
| ![bad_man_with_gun](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_3_hobo_symbols/bad_man_with_gun_lives_here.png) | ![kind_woman_lives_here](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_3_hobo_symbols/kind_woman_lives_here.png) | ------------- | ------------- |
| ![safe_camp](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_3_hobo_symbols/safe_camp.png) | ![courthouse](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_3_hobo_symbols/courthouse.png) | | ------------- | ------------- |
 ![dangerous_drinking_water](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_3_hobo_symbols/dangerous_drinking_water.png) | ![doctor](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_3_hobo_symbols/doctor.png)

Guidebook pages:

[Page 3: Hobo Signs](http://historysurvivalguide.com/page/hobo-signs-and-symbols-part-one/)

[Page 4: Hobo Signs](http://historysurvivalguide.com/page/hobo-signs-and-symbols-part-two/)

[Page 5: Hobo Signs](http://historysurvivalguide.com/page/hobo-signs-and-symbols-part-three/)

[Page 6: Hobo Signs](http://historysurvivalguide.com/page/hobo-signs-and-symbols-part-four/)

### [Page 10-12: Pioneer Plaque](https://github.com/cyschneck/History-Survival-Guide/tree/master/page_10_pioneer_plaque)

Clean PNG of the Pioneer Plaque

![pioneer_plaque+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_10_pioneer_plaque/full_scale_pioneer_plaque.png)

Reuse of this image is governed by [NASA's image use policy](https://www.nasa.gov/multimedia/guidelines/index.html).

 <p align="center">
  <img src="https://github.com/cyschneck/History-Survival-Guide/blob/master/page_10_pioneer_plaque/full_scale_diagram.jpg" />
</p>

[Page 10: Pioneer Plaque](http://historysurvivalguide.com/page/pioneer-plaque-part-1/)

[Page 11: Pioneer Plaque](http://historysurvivalguide.com/page/pioneer-plaque-part-2/)

[Page 12: Pioneer Plaque](http://historysurvivalguide.com/page/pioneer-plaque-part-3/)

### [Page X: Astrolabe](https://github.com/cyschneck/History-Survival-Guide/tree/master/page_x_astrolabe)

Currently uses: Python 3.7.3

**Constructing a Base Plate**

Base plate includes the position of the Tropic of Cancer, Tropic of Capricorn, and the Equator in three concentric circles. The position of each circle is due to the obliquity of the planet and over time the obliquity of Earth can shift

Corrected for obliquities between 0°-89.99° (undefined at 90°) when radius of base plate is 1

```python3 generate_base_plate.py```

```
outer_tropic_radius = base_plate_radius
equator_radius = base_plate_radius / (tan(45° + (obliquity / 2))
inner_tropic_radius = base_plate_radius / (tan(45° - (obliquity / 2))
```
![change_in_obliquity_radius+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/generate_base_plate_outputs/base_plate_change_due_to_obliquity.png)
![earth_base_plate+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/generate_base_plate_outputs/base_plate_for_earth_at_23.4_degrees.png)

__TO BE MOVED IN PYPY__

Currently, [vondrak plugin](https://github.com/digitalvapor/vondrak) can only run on python2.7 (using Python 2.7.12)

```python2.7 test_precession.py```
![test_prcession_star+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/test_precession_vondrak_example.png)

**Constructing Eccentric Calendar for Back Plate**

An eccentric calendar assumes the sun moves at a constant speed throughout the year but accounts for the Sun's true anomaly as an offset from the Vernal Equinox. Due to both *longitude* and the *year since 2000*, the center of the calendar will be placed at an offset from the center of the back plate of the astrolabe on the line of apsides (the line connecting the perihelion and aphelion)

Code will generate both the angular distance from the Vernal Equinox to the January 0 (midnight of December 31) at the beginning of the year as well as the offset (x, y) from the center of the back plate

```python3 calculate_eccentric_calendar_offset.py```

Variables:
1. Year to calculate (for example: 2023)
2. The longitude of the observer (-71.05° for Boston, -105.27° for Boulder, 0° for Greenwich, 13.74° for Dresden)
3. Radius of the back plate

```
For the Year 2023 at longitude -105.2705° for a plate with a radius of 1.0

Perihelion = 103.332864°
Aphelion   = 283.332864°
Mean Anomaly of Jan 0 = 357.310661°
Line of Apside relative to Vernal Equinox for Longitude -105.2705° = -79.64488807474879°

Offset due to Eccentricity with radius of 1.0 = 0.033398
X offset with radius of 1.0 = -0.007702
Y offset with radius of 1.0 = 0.032498
```
_How Changing the Year Changes Eccentricity_
![change_in_year_eccentricity+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_year_versus_eccentricity.png)
_How Changing the Year Changes the Offset (X, Y)_
![change_in_year_offset+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_year_versus_offset.png)
_How Changing the Longitude Changes the Angular Distance to the Vernal Equinox_
![change_in_longitude_angular_distance+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_longitude_versus_angular_distance.png)

**Generate Star Chart**

 Generate a star chart with spherical projection for the rete at [cyschneck.pythonanywhere.com](http://cyschneck.pythonanywhere.com/) based on [Star-Chart-Spherical-Projection](https://github.com/cyschneck/Star-Chart-Spherical-Projection)
 
 
_Example outputs:_

__Star Chart in the Northern Hemisphere (centered on 90°) without Precession__
![north_star_chart_without_labels_without_precession+png](https://raw.githubusercontent.com/cyschneck/Star-Chart-Spherical-Projection/main/examples/north_without_labels_without_precession.png) 
![north_star_chart_with_labels_without_precession+png](https://raw.githubusercontent.com/cyschneck/Star-Chart-Spherical-Projection/main/examples/north_with_labels_without_precession.png) 
__Star Chart in the Northern Hemisphere (centered on 90°) with Precession__
![north_star_chart_without_labels_with_precession+png](https://raw.githubusercontent.com/cyschneck/Star-Chart-Spherical-Projection/main/examples/north_without_labels_with_precession.png) 
![north_star_chart_with_labels_with_precession+png](https://raw.githubusercontent.com/cyschneck/Star-Chart-Spherical-Projection/main/examples/north_with_labels_with_precession.png) 

__Star Chart in the Southern Hemisphere (centered on -90°) without Precession__
![south_star_chart_without_labels_without_precession+png](https://raw.githubusercontent.com/cyschneck/Star-Chart-Spherical-Projection/main/examples/south_without_labels_without_precession.png) 
![south_star_chart_with_labels_without_precession+png](https://raw.githubusercontent.com/cyschneck/Star-Chart-Spherical-Projection/main/examples/south_with_labels_without_precession.png) 
__Star Chart in the Southern Hemisphere (centered on -90°) without Precession__
![south_star_chart_without_labels_with_precession+png](https://raw.githubusercontent.com/cyschneck/Star-Chart-Spherical-Projection/main/examples/south_without_labels_with_precession.png) 
![south_star_chart_with_labels_with_precession+png](https://raw.githubusercontent.com/cyschneck/Star-Chart-Spherical-Projection/main/examples/south_with_labels_with_precession.png) 
