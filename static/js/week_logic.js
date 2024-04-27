            
    dayarray = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];

    function render_week(render_day){

        // Get the list of meetings for the render_day
        meetings = return_weeks_meetings(render_day);
        // select the container for html injection
        const show_week = document.querySelector(".container1");

        // Find monday of the week that render_day is in 
        minday = new Date(render_day.getFullYear(),render_day.getMonth(),render_day.getDate()-render_day.getDay());

        week_days = [];
        day_index = 0; // keep track of which day of the week we are on 
        for (i in dayarray){
            tempa = [];
                count = 0;
                offset = 10; // offset for each visual meeting 

                // Itterate through all of the meetings in that day, then create a string of html items that wie will append to the container 
                for (let m of parceMeetingTimes(day_index, meetings)) {
                    tempa += `<div class = a
                    style = "
                    position:absolute; 
                    background-color: rgb(68, 158, 123);
                    width: 20px;
                    height: ${parceSize(m.start, m.end)}px;
                    margin-left: ${offset}px; 
                    margin-top: ${barPosition(m.start)}px;
                    border-radius: 5px;">
                    </div>`;
                    count++;
                    offset = offsetCal(offset, 20, 10, 140);
                }
            
            // Create an HTML item that will represent a column for each day, we will append the tempa array inside of 
            // the  HTML code for the column so that each column will get HTML items for all of the meetings 
            week_days += `<div class="column">
            <h2>${dayarray[i]}</h2>
            <p1>${(minday.getMonth()+1) + "/" + minday.getDate()}</p1>
            <div class="${dayarray[i]}">${tempa}</div>
            <style>.${dayarray[i]} {
            background-color: rgb(190, 193, 204);
            width: 150px; /* Each canvas occupies 1/7th of the container's width */
            height: 94%;
            border-radius: 10px;}
            </style></div>`
            minday.setDate(minday.getDate()+1);
            day_index++;
        }
        show_week.innerHTML = week_days;
        }
    function addLineSubPath(ctx, y) {
        ctx.moveTo(0, y);
        ctx.lineTo(200, y);
    }

    function offsetCal(offsetcurr, width, startpos, endpos){
        var offset = offsetcurr;
        var direction = 0;

        if (offset > endpos) {
            direction = 1;
        }
        else if (offset < startpos) {
            direction = 0;
        }

        if(offset <= endpos && direction == 0) {
            offset = offset + (width + 5);
        }
        else if (offset >= startpos && direction == 1) {
            offset = offset - (width + 5);
        }
        return offset;
    }

    function barPosition(dateTimeStart) {
        var date1 = new Date(dateTimeStart); 
        var date2 = new Date(dateTimeStart);
        date2.setHours(0);
        date2.setMinutes(0);
        date2.setSeconds(0);
        var differenceMs = date1.getTime() - date2.getTime();
        var hours = differenceMs / (1000 * 60 * 60);
        var pos = 1200 * (hours/24);
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
        var size = 1200 * (hours/24);

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