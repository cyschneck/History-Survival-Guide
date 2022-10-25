# History Survival Guide
### A Time Traveler’s Guide to Surviving History

![Banner_Light](https://user-images.githubusercontent.com/22159116/64215868-b84b1500-ce73-11e9-98fc-4cac0c190fc4.jpg)

**About This Project**

This is a science and history blog that explores scientific concepts coupled with practical information about how to recreate and use the techniques described by hand.  The History Survival Guide (or,  A Time Traveler’s Guide to Surviving History) has been updating since July 2019. Each page is the accumulation of research for a particular topic, synthesized and summarized in a useful ‘survival guide’ format. So far, topics covered included using the proper motion of stars to determine what time period a time traveler could have found themselves in, deciphering ‘Hobo Symbols’ from the 1800’s, reading the Pioneer Plaque, and constructing an astrolabe from scratch. All pages are done in a pulp science fiction aesthetic.

This github repo includes all relevant code and images used in a given guidebook page

[historysurvivalguide.com](http://historysurvivalguide.com/)

[Behind the Scenes - Tumblr](https://historysurvivalguide.tumblr.com/)

### [Page 1: Proper Motion](https://github.com/cyschneck/History-Survival-Guide/tree/master/page_1_proper_motion)
Determine Angular Motion Between Two Given Stars

Included:
* Python code to determine the angular distance between two Stars

Guidebook page:

[Page 1: Proper Motion](http://historysurvivalguide.com/page/determine-eon-proper-motion/)

### [Page 3-6: Hobo Symbols](https://github.com/cyschneck/History-Survival-Guide/tree/master/page_3_hobo_symbols)
Hobo Signs and Symbols with definitions

Included:
* Each individual Hobo symbols (png), 248 x 248 pixels that is formatted for Slack
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

[Page 10: Pioneer Plaque](http://historysurvivalguide.com/page/pioneer-plaque-part-1/)

[Page 11: Pioneer Plaque](http://historysurvivalguide.com/page/pioneer-plaque-part-2/)

[Page 12: Pioneer Plaque](http://historysurvivalguide.com/page/pioneer-plaque-part-3/)

### [Page X: Astrolabe](https://github.com/cyschneck/History-Survival-Guide/tree/master/page_x_astrolabe)

**Constructing a Base Plate**

Base plate includes the position of the Tropic of Cancer, Tropic of Capricorn, and the Equator in three concentric circles. The position of each circle is due to the obliquity of the planet

Corrected for obliquities between 0°-89.99° (undefined at 90°) when radius of base plate is 1

```
outer_tropic_radius = base_plate_radius
equator_radius = base_plate_radius / (tan(45° + (obliquity / 2))
inner_tropic_radius = base_plate_radius / (tan(45° - (obliquity / 2))
```

![change_in_obliquity_radius+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/generate_base_plate_outputs/base_plate_change_due_to_obliquity.png)
![earth_base_plate+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/generate_base_plate_outputs/base_plate_for_earth_at_23.4_degrees.png)

**Constructing a Star Chart**

Currently includes 62 stars in both the North and South Hemisphere

```python3 generate_star_chart.py```

Currently uses: Python 3.7.3

Optional Variables:
1. North or South Hemisphere (and range of declination values, default between -30°-90° N and -90°-30° S) centered on +90° or -90° pole
2. Filter based on the Visual Magnitude of a star (-2 brightest, 10 dimmest)
3. Proper Motion based on time since 2000
5. Optional labels for Stars and Declination Values
6. Precession of the Equinoxes

**North Hemisphere**
![north_star_chart_without_precession_with_labels+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/star_chart_north_without_precession_with_labels.png)
![north_star_chart_without_precession_without_labels+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/star_chart_north_without_precession_without_labels.png)
![north_star_chart_with_precession_with_labels+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/star_chart_north_with_precession_with_labels.png)
![north_star_chart_with_precession_without_labels+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/star_chart_north_with_precession_without_labels.png)
**South Hemisphere**
![south_star_chart_without_precession_with_labels+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/star_chart_south_without_precession_with_labels.png)
![south_star_chart_without_precession_without_labels+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/star_chart_south_without_precession_without_labels.png)
![south_star_chart_with_precession_with_labels+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/star_chart_south_with_precession_with_labels.png)
![south_star_chart_with_precession_without_labels+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/star_chart_south_with_precession_without_labels.png)

Precession of Equinoxes based on Time since 2000

Implementation of "New precession expressions, valid for long time intervals" (J. Vondrak, N. Capitaine, and P. Wallace) (2011)

Currently, [vondrak plugin](https://github.com/digitalvapor/vondrak) can only run on python2.7 (using Python 2.7.12)

```python2.7 test_precession.py```
![test_prcession_star+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/test_precession_vondrak_example.png)

**Constructing Eccentric Calendar for Back Plate**

An eccentric calendar assumes the sun moves at a constant speed throughout the year and accounts for the Sun's true anomaly as an offset from the Vernal Equinox. Due to both *longitude* and the *year since 2000*, the center of the calendar will be placed at an offset from the center of the back plate of the astrolabe on the line of apsides (the line connecting the perihelion and aphelion)

Code will generate both the angular distance from the Vernal Equinox to the January 0 (midnight of December 31) at the beginning of the year as well as the offset (x, y) from the center of the back plate

```python3 calculate_eccentric_calendar_offset.py```

Variables:
1. Year to calculate (for example: 2022)
2. The longitude of the observer (-71.05° for Boston, -105.27° for Boulder, 0° for Greenwich, 13.74° for Dresden)
3. Radius of the back plate

For the Year 2022 at longitude -105.2705 for a plate with a radius of 1

```
Perihelion = 103.315666°
Aphelion   = 283.315666°
Mean Anomaly of Jan 0 = 357.320158°

Line of Apside relative to Vernal Equinox for Longitude -105.2705° = -79.65258771051492°

X offset with radius of 1 = -0.007679
Y offset with radius of 1 = 0.032445
```
_How Changing the Year Changes Eccentricity_
![change_in_year_eccentricity+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_year_versus_eccentricity.png)
_How Changing the Year Changes the Offset (X, Y)_
![change_in_year_offset+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_year_versus_offset.png)
_How Changing the Longitude Changes the Angular Distance to the Vernal Equinox_
![change_in_longitude_angular_distance+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_astrolabe/calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_longitude_versus_angular_distance.png)

### [Page X: Equation of Time](https://github.com/cyschneck/History-Survival-Guide/tree/master/page_x_equation_of_time)

**Effect of Eccentricity**
![earth_effect_of_eccentricity+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_equation_of_time/eot_graphs/eccentricity/earth_eot_effect_of_eccentricity.png)
![eccentricity_change_in_time_EOT+png](https://github.com/cyschneck/History-Survival-Guide/blob/master/page_x_equation_of_time/eot_graphs/eccentricity/change_in_time_due_to_eccentricity.png)

**Effect of Obliquity**

**TODO: Graph Effect of Obliquity**

