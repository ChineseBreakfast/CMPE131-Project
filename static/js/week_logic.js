            //var MeetingsM = parceMeetingTimes(1, meetings);
            //var MeetingsT = parceMeetingTimes(2, /*python function here*/);
            //var MeetingsW = parceMeetingTimes(3, /*python function here*/);
            //var MeetingsTh = parceMeetingTimes(4, /*python function here*/);
            //var MeetingsF = parceMeetingTimes(5, /*python function here*/);
            //var MeetingsSa = parceMeetingTimes(6, /*python function here*/);
            //var MeetingsSu = parceMeetingTimes(0, /*python function here*/);
            //console.log("Meetings: ", MeetingsM);

    function render_week(render_day){
        const show_week = document.querySelector(".container1");
        minday = new Date(render_day.getFullYear(),render_day.getMonth(),render_day.getDate()-render_day.getDay());
        week_days = `<div class="column"><h2>Sunday</h2><p1>${(minday.getMonth()+1) + "/" + minday.getDate()}</p1><canvas id="Sunday" style="border:1px solid grey"></canvas></div>`
        minday.setDate(minday.getDate()+1);
        week_days += `<div class="column"><h2>Monday</h2><p1>${(minday.getMonth()+1) + "/" + minday.getDate()}</p1><canvas id="Monday" style="border:1px solid grey"></canvas></div>`
        minday.setDate(minday.getDate()+1);
        week_days += `<div class="column"><h2>Tuesday</h2><p1>${(minday.getMonth()+1) + "/" + minday.getDate()}</p1><canvas id="Tuesday" style="border:1px solid grey"></canvas></div>`
        minday.setDate(minday.getDate()+1);
        week_days += `<div class="column"><h2>Wednesday</h2><p1>${(minday.getMonth()+1) + "/" + minday.getDate()}</p1><canvas id="Wednesday" style="border:1px solid grey"></canvas></div>`
        minday.setDate(minday.getDate()+1);
        week_days += `<div class="column"><h2>Thursday</h2><p1>${(minday.getMonth()+1) + "/" + minday.getDate()}</p1><canvas id="Thursday" style="border:1px solid grey"></canvas></div>`
        minday.setDate(minday.getDate()+1);
        week_days += `<div class="column"><h2>Friday</h2><p1>${(minday.getMonth()+1) + "/" + minday.getDate()}</p1><canvas id="Friday" style="border:1px solid grey"></canvas></div>`
        minday.setDate(minday.getDate()+1);
        week_days += `<div class="column"><h2>Saturday</h2><p1>${(minday.getMonth()+1) + "/" + minday.getDate()}</p1><canvas id="Saturday" style="border:1px solid grey"></canvas></div>`
        show_week.innerHTML = week_days;

        meetings = return_weeks_meetings(render_day);
        
        var MeetingsM = parceMeetingTimes(1, meetings);
        var MeetingsT = parceMeetingTimes(2, meetings);
        var MeetingsW = parceMeetingTimes(3, meetings);
        var MeetingsTh = parceMeetingTimes(4, meetings);
        var MeetingsF = parceMeetingTimes(5, meetings);
        var MeetingsSa = parceMeetingTimes(6, meetings);
        var MeetingsSu = parceMeetingTimes(0, meetings);

        console.log("Meetings: ", meetings);
        console.log("Meetings: ", MeetingsM);

            const cM = document.getElementById("Monday");
            const ctxM = cM.getContext("2d");
            //ctxM.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxM.height = window.innerHeight * 0.5; // 80% of window height
            
            offset = 10;
            for (let m of MeetingsM) {
                ctxM.fillStyle = "red";
                ctxM.fillRect(offset, barPosition(m.start), 20, parceSize(m.start, m.end));
                offset = offset + 25;
            }

            
            
            const cT = document.getElementById("Tuesday");
            const ctxT = cT.getContext("2d");
            //ctxT.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxT.height = window.innerHeight * 0.5; // 80% of window height
            
            offset = 10;
            for (let m of MeetingsT) {
                ctxT.fillStyle = "red";
                ctxT.fillRect(offset, barPosition(m.start), 20, parceSize(m.start, m.end));
                offset = offset + 25;
            }



            const cW = document.getElementById("Wednesday");
            const ctxW = cW.getContext("2d");
            //ctxW.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxW.height = window.innerHeight * 0.50; // 80% of window height
            
            offset = 10;
            for (let m of MeetingsW) {
                ctxW.fillStyle = "red";
                ctxW.fillRect(offset, barPosition(m.start), 20, parceSize(m.start, m.end));
                offset = offset + 25;
            }



            const cTh = document.getElementById("Thursday");
            const ctxTh = cTh.getContext("2d");
            //ctxTh.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxTh.height = window.innerHeight * 0.50; // 80% of window height
            
            offset = 10;
            for (let m of MeetingsTh) {
                ctxTh.fillStyle = "red";
                ctxTh.fillRect(offset, barPosition(m.start), 20, parceSize(m.start, m.end));
                offset = offset + 25;
            }



            const cF = document.getElementById("Friday");
            const ctxF = cF.getContext("2d");
            //ctxF.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxF.height = window.innerHeight * 0.50; // 80% of window height
            
            offset = 10;
            for (let m of MeetingsF) {
                ctxF.fillStyle = "red";
                ctxF.fillRect(offset, barPosition(m.start), 20, parceSize(m.start, m.end));
                offset = offset + 25;
            }



            const cSa = document.getElementById("Saturday");
            const ctxSa = cSa.getContext("2d");
            //ctxSa.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxSa.height = window.innerHeight * 0.50; // 80% of window height
            
            offset = 10;
            for (let m of MeetingsSa) {
                ctxSa.fillStyle = "red";
                ctxSa.fillRect(offset, barPosition(m.start), 20, parceSize(m.start, m.end));
                offset = offset + 25;
            }



            const cSu = document.getElementById("Sunday");
            const ctxSu = cSu.getContext("2d");
            //ctxSu.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxSu.height = window.innerHeight * 0.50; // 80% of window height
            
            offset = 10;
            for (let m of MeetingsSu) {
                ctxSu.fillStyle = "red";
                ctxSu.fillRect(offset, barPosition(m.start), 20, parceSize(m.start, m.end));
                offset = offset + 25;
            }
        }
            //window.addEventListener('resize', domloaded);
    function barPosition(dateTimeStart) {
        var date1 = new Date(dateTimeStart); 
        var date2 = new Date(dateTimeStart);
        date2.setHours(0);
        date2.setMinutes(0);
        date2.setSeconds(0);
        var differenceMs = date1.getTime() - date2.getTime();
        var hours = differenceMs / (1000 * 60 * 60);
        var pos = 150 * (hours/24);
        return pos;
    }

    function parceSize(dateTimeStart, dateTimeEnd){
        /*Range Date*/
        // Parse the time strings into Date objects
        var date1 = new Date(dateTimeStart); 
        var date2 = new Date(dateTimeEnd);

        // Calculate the difference in milliseconds
        var differenceMs = date2.getTime() - date1.getTime();

        // Convert the difference into hours, minutes, and seconds
        var hours = differenceMs / (1000 * 60 * 60);

        // Convert hours into an integer as a size of the bar on the canvas
        var size = 150 * (hours/24);

        // Return the difference as an object
        return size;
        }

    function getDateForDayOfWeek(dayOfWeek, setTimeToMidnight) {
        // Get the current date
        var currentDate = new Date();
        // Get the current day of the week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
        var currentDayOfWeek = currentDate.getDay();
        // Get the target day of the week as an integer (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
        var targetDayOfWeek = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'].indexOf(dayOfWeek.toLowerCase());
    
        // Calculate the difference in days between the current day and the target day
        var daysUntilTargetDay = (targetDayOfWeek - currentDayOfWeek + 7) % 7;
    
        // Add the difference in days to the current date
        currentDate.setDate(currentDate.getDate() + daysUntilTargetDay);
    
        // Set the time to either 0:00 or 24:00
        if (setTimeToMidnight) {
            currentDate.setHours(0, 0, 0, 0); // Set time to 0:00
        } else {
            currentDate.setHours(23, 59, 59, 999); // Set time to 23:59:59.999
        }
    
        return currentDate;
    }

    function parceMeetingTimes(day, Meetings) {
        var MeetingsDay = [];
        for (let m of Meetings) {
            var d = new Date(m.start);
            if(d.getDay() == day) {
                MeetingsDay.push(m);
            }
          }
        return MeetingsDay;
    }

    const today1 = new Date();
    render_week(today1);