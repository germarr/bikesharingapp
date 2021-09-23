document.addEventListener("DOMContentLoaded", function(){
    // Fake Data
    const cardOne=[{
        "title":"Total Trips",
        "cardsData":[3000000],
        "cardsCompare": [2000000],
        "compareList":[]
    },
    {
        "title":"Avg. Time",
        "cardsData":[10.12],
        "cardsCompare": [21.15],
        "compareList":[]
    },
    {
        "title":"Avg. Distance per Trip",
        "cardsData":[1.42],
        "cardsCompare": [1.38],
        "compareList":[]
    },
    {
        "title":"Total kms.",
        "cardsData":[20.42],
        "cardsCompare": [18.38],
        "compareList":[]
    },
    {
        "title":"Revenue",
        "cardsData":[200],
        "cardsCompare": [100],
        "compareList":[]
    }]

    //console.log(cardOne[0])
    
    // Card Function
    function card1(num){
        for (let i = 0; i < cardOne[num].cardsData.length; i++) {
            cardOne[num].compareList.push(((cardOne[num].cardsData[i]-cardOne[num].cardsCompare[i])/cardOne[num].cardsCompare[i])*100)
        }

        if(cardOne[num].compareList[0] >= 0){
            document.querySelector(`#card${num+1}Color`).className = "bg-green-200 mt-2 ml-3 rounded-xl p-2";
            document.querySelector(`#card${num+1}Compare`).className="text-xs font-semibold text-green-800";
        }else{
            document.querySelector(`#card${num+1}Color`).className = "bg-red-200 mt-2 ml-3 rounded-xl p-2";
            document.querySelector(`#card${num+1}Compare`).className="text-xs font-semibold text-red-800";
        }
    
        document.querySelector(`#card${num+1}Title`).innerHTML = cardOne[num].title;
        document.querySelector(`#card${num+1}`).innerHTML = cardOne[num].cardsData[0].toLocaleString();
        document.querySelector(`#card${num+1}Compare`).innerHTML = `${Number.parseFloat(cardOne[num].compareList[0]).toPrecision(3)} %`

    }
    card1(num=0)
    card1(num=1)
    card1(num=2)
    card1(num=3)
    card1(num=4)

    // TOP BAR CHART
    function activateChart(){
        let dataList = [0, 10, 5, 2, 20, 30, 45];
        let datalabels = ['January','February','March','April','May','June'];
        
        const chartbar = new Chart(document.getElementById('barAge').getContext('2d'),{
            type: 'line',
            data:{
                labels: datalabels,
                datasets: [{
                    label: 'My First dataset',
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: dataList,
                }]},
            options: {
                maintainAspectRatio:false,
                scales:{
                    y:{
                        grid:{
                            display:false
                        }
                    },
                    x:{
                        grid:{
                            display:false
                        }
                    }
                }
            }});
    }
    
    activateChart();
    
    //Table of Stations.
    function buildTable(){
        
        const table = document.querySelector("table");
        
        for(let i = 1; i < 10; i++){
            let row = table.insertRow(i)
            // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
    
            // Add some text to the new cells:
            cell1.innerHTML = "Cell 1";
            cell2.innerHTML = "Cell 2";
            cell3.innerHTML = "Cell 3";
        }
    }

    buildTable()

    //Building a Map
    const mymap = L.map('mapid').setView([19.373142, -99.17828], 15);
    const marker = L.marker([0, 0]).addTo(mymap);
    marker.setLatLng([19.373142, -99.17828])
    var polylinePoints = [
            [19.443928, -99.15253],
            [19.3586, -99.1561]
        ];            
        
    var polyline = L.polygon(polylinePoints).addTo(mymap);

    var circle = L.circle([19.373142, -99.17828], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 500
    }).addTo(mymap);

    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png?{foo}', {foo: 'bar', attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'});
    tiles.addTo(mymap);

    
    // DONUT CHART
    const genderData = {
        labels: ["M","F","X"],
        datasets: [{
            label: 'My First Dataset',
            data: [60,35,5],
            backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
            ],
            hoverOffset: 4
        }]
    }

    const genderConfig = {
        plugins:[ChartDataLabels],
        type: 'doughnut',
        data:genderData,
        options: {
            tooltips:{
                enabled:false
            },
            plugins:{
                datalabels:{
                    formatter: function(value, context) {
                        return context.chart.data.datasets[0].data[context.dataIndex] + '%';
                    },
                    display:true,
                    align:"center",
                    color:"white",
                    labels:{
                        title:{
                            font:{
                                size:15,
                                weight:"bold"
                            }
                        }
                    },
                    value:{
                        color:"green"
                    }
                },
            },
            maintainAspectRatio: true
        }
    }

    const donutchart = new Chart(document.getElementById('donutchart').getContext('2d'),genderConfig)

    // WEEK BAR CHART
    const barData = {
        labels: ['MON','TUE','WED','THUR','FRI','SAT', 'SUN'],
        datasets: [{
            label: 'Trips per Hour',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45,11],
        }]
    }

    const barConfig = {
        type: 'bar',
        data:barData,
        options: {
            indexAxis:'y',
            maintainAspectRatio:false,
            scales:{
                y:{
                    grid:{
                        display:false
                    },
                    title:{
                        display: true,
                        text:"Hour"
                    } 
                },
                x:{
                    grid:{
                        display:false
                    },
                    title:{
                        display: true,
                        text:"# of Trips"
                    } 
                },
            }
        }
    }

    const chartbar = new Chart(document.getElementById('barWeek').getContext('2d'),barConfig);
        
    function yearsSelect(){
        const years = [2019,2020,2021];

        for (let i = 0; i < years.length; i++) {
            const selectItem = document.createElement("option");
            selectItem.setAttribute("value", `${years[i]}`);
            selectItem.innerHTML = years[i];
            document.querySelector("#selectYears").append(selectItem);
        }

        const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dic"];

        for (let i = 0; i < months.length; i++) {
            const selectMonth = document.createElement("option");
            selectMonth.setAttribute("value", `${i+1}`);
            selectMonth.innerHTML = months[i];
            document.querySelector("#selectMonths").append(selectMonth);
        }

        const days = [...Array(31).keys()]
        
        for (let i = 0; i < 31; i++) {
            const selectDays = document.createElement("option");
            selectDays.setAttribute("value", `${String(i+1)}`)
            selectDays.innerHTML = String(i+1);
            document.querySelector("#selectDays").append(selectDays);
        }
    }

    yearsSelect();
        
        
    // SEARCH BUTTON
    document.querySelector("#searchbutton").onclick = function(){
        // console.log("Yas")
        let formYear = document.querySelector("#selectYears").value;
        let fromMonth = document.querySelector("#selectMonths").value;
        let formDay = document.querySelector("#selectDays").value;
        let dayofYear;
        let dayofweek;
        let dayofmonth;
        let querypt2;

        if(parseInt(formDay) < 10){
            dayofweek = `0${formDay}`
        }else{
            dayofweek = `${formDay}`
        }

        if(parseInt(fromMonth) < 10){
            dayofmonth = `0${fromMonth}`
        }else{
            dayofmonth = `${fromMonth}`
        }

        if(dayofmonth==="All" & dayofweek==="All"){
            querypt2 = ""
        }else if(dayofmonth!="All" & dayofweek==="All"){
            querypt2 = `?trip_month=${dayofmonth}`
        }else if(dayofmonth==="All" & dayofweek!="All"){
            querypt2 = `?trip_day=${dayofweek}`
        }else{
            querypt2 = `?trip_month=${dayofmonth}&trip_day=${dayofweek}`
        }

        if(dayofYear==="All"){
            dayofYear = 2000
        }else{
            dayofYear = formYear
        }
        

        console.log(`http://localhost:8888/cards/${dayofYear}${querypt2}`);

        
        
        async function catchData(){
            const response = await fetch(`http://localhost:8888/cards/${dayofYear}${querypt2}`);
            const answer = await response.json() 
            let cardsData = await answer["cardsData"][0]
            let hourlyTrip = await answer["hourly_trips"]
            let topRoutes = await answer["top_routes"]
            let genderData = await answer["gender"]
            let locations = await answer["top_locations"]
            let stations = await answer["stations"]
            
            console.log(">>>",stations["stations"][0][0])

            //document.querySelector("#exampleID").innerHTML = answer["results"][1]["name"];
            document.querySelector("#card1").innerHTML = cardsData["total_trips"].toLocaleString();
            document.querySelector("#card2").innerHTML = cardsData["avg_time"];
            document.querySelector("#card3").innerHTML = cardsData["avg_distance"];
            document.querySelector("#card4").innerHTML = cardsData["total_kms"].toLocaleString();
            document.querySelector("#card5").innerHTML = cardsData["total_revenue"].toLocaleString();

            //Update Time Chart
            chartbar.data.datasets[0].data= hourlyTrip["tripsPerHour"];
            chartbar.data.labels= hourlyTrip["hourly"];
            chartbar.update();

            // Update Donut Chart
            let nameX;
            let nameXI;

            if(genderData[2]){
                console.log("TRUE")
                nameX = genderData[2]["counts"]
                nameXI = genderData[2]["genero_usuario"]
                donutchart.data.datasets[0].data= [genderData[0]["counts"],genderData[1]["counts"], nameX]
                donutchart.data.labels= [genderData[0]["genero_usuario"],genderData[1]["genero_usuario"],nameXI];
                donutchart.update();
            }else{
                console.log("FALSE")
                donutchart.data.datasets[0].data= [genderData[0]["counts"],genderData[1]["counts"]]
                donutchart.data.labels= [genderData[0]["genero_usuario"],genderData[1]["genero_usuario"]];
                donutchart.update();
            }

            

            //Update Table
            const table = document.querySelector("table");
            
            for(let i = 1; i < 10; i++){
                table.deleteRow(i)
                let row = table.insertRow(i)
                // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
        
                // Add some text to the new cells:
                cell1.innerHTML = topRoutes["name_retiro"][i];
                cell2.innerHTML = topRoutes["name_arribo"][i];
                cell3.innerHTML = topRoutes["counts"][i];
            }

            //Update Map
            document.querySelector('#mapid').remove()

            const selectMap= document.createElement("div");
            selectMap.setAttribute("id", "mapid");
            document.querySelector("#maxMap").append(selectMap)

            const mymapII = L.map('mapid').setView([locations["name_retiro"][0][0], locations["name_retiro"][0][1]], 13);
            const tilesII = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png?{foo}', {foo: 'bar', attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'});
            tilesII.addTo(mymapII);


            for (var i = 0; i < locations["name_arribo"].length; i++) {
                    let polyline = L.polyline([[locations["name_retiro"][i][0],locations["name_retiro"][i][1]],[locations["name_arribo"][i][0],locations["name_arribo"][i][1]]])
                    .addTo(mymapII);
            }
            for (var i = 0; i < stations["stations"].length; i++) {
                let circle = L.circle([stations["stations"][i][0], stations["stations"][i][1]], {
                color: '#4B6587',
                fillColor: '#FFEBA1',
                fillOpacity: 0.5,
                radius: 50
            })
            .addTo(mymapII);}
            
            
            return false
        }  

        catchData();
        
    }

})


