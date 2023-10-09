# GGDH Dashboard Ver 3.0

New in ver 3.0:

1. Updated data from 2009 to 2022 (some datasets only have certain years of data)
2. Updated search and filter bar to select certain neighbourhood
3. Move the Year slider up
4. The year slider corresponds to the data availability

Things that need to be fixed:
1. Liedschendam-Voorburg "Wijk" is still not correct.
2. Add new 2021 data




Link :

https://ggdh-ver-1-0.onrender.com/

This is one of the dashboard project prototype for GGDH / HHTH-ELAN from the department of public health and primary care at LUMC / Health Campus the Hague.
In the current version, there are few notes that we need to be aware of :

1. The care products (themes) is not up to date yet. In the future, we are planning to include different themes for every button which corresponds to the "variables" that can be chosen in the dropdown menu, visualization and comments / text

2. The dropdown menu selection is still not yet cover the full range of what we have in the our data environment

3. The "Overall" or summary of each healthcare cost it is not according to the real data. and currently summarize of the region that is chosen from the dropdown menu below it. 

4. The choropleth map use "wijk"/ district as the level agregation of the visualization and the region is based on the dropdown menu chosen for the area. In the future, we are planning to differ the level of aggregation for sprecific region choosen. For example, we can chhose "gementee"/ muncipality level of agregation if we chose ROAZ region. 

5. The bar chart is already ordered based on the variable chosen from the dropdown menu. underneath it, we have some notes/ comments section on what intersting about the visualization so far. However, the comments is not yet filled with meaningful insight

6. the line chart (trendline) on the left (section 3) is based on the "clicked region of th map. So, if you click in region of Centrum. it will show region of centrum trendline of variable that is choosen in the section 2. however, the the yearly data is not yet there, So we cannot link the "click map" function to the trendline.

7. we also add the trendline for every lowest level zone that is chosen from the area (from the section 2 - e.g. Roaz/ per neighbourhood). Later, we will do a little bit of time series clustering to group each zone trendline to label them per colour according to their trendline pattern. 

8. Lastly, we add a little bit of footer regarding person/contact that made the dashboard and we also put some kind of hyperlink for the datasource and the explanation of each variables that are in the dropdown menu. (not yet)

-- Ammar, Frank, Jeroen, Marc


