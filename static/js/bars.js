        
    document.addEventListener('DOMContentLoaded',domloaded,false);
    function domloaded(){
            
            //var MeetingsM = parceMeetingTimes(1, /*python function here*/);
            //var MeetingsT = parceMeetingTimes(2, /*python function here*/);
            //var MeetingsW = parceMeetingTimes(3, /*python function here*/);
            //var MeetingsTh = parceMeetingTimes(4, /*python function here*/);
            //var MeetingsF = parceMeetingTimes(5, /*python function here*/);
            //var MeetingsSa = parceMeetingTimes(6, /*python function here*/);
            //var MeetingsSu = parceMeetingTimes(0, /*python function here*/);
            //console.log("Meetings: ", MeetingsM);

            const cM = document.getElementById("Monday");
            const ctxM = cM.getContext("2d");
            //ctxM.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxM.height = window.innerHeight * 0.5; // 80% of window height
            x = 150;
            offset = 10;
            for (let i = 0; i < 3; i++) {
                ctxM.fillStyle = "red";
                ctxM.fillRect(offset, 0, 20, x);
                offset = offset + 25;
            }

            
            
            const cT = document.getElementById("Tuesday");
            const ctxT = cT.getContext("2d");
            //ctxT.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxT.height = window.innerHeight * 0.5; // 80% of window height
            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxT.fillStyle = "red";
                ctxT.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }



            const cW = document.getElementById("Wednesday");
            const ctxW = cW.getContext("2d");
            //ctxW.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxW.height = window.innerHeight * 0.50; // 80% of window height
            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxW.fillStyle = "red";
                ctxW.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }



            const cTh = document.getElementById("Thursday");
            const ctxTh = cTh.getContext("2d");
            //ctxTh.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxTh.height = window.innerHeight * 0.50; // 80% of window height
            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxTh.fillStyle = "red";
                ctxTh.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }



            const cF = document.getElementById("Friday");
            const ctxF = cF.getContext("2d");
            //ctxF.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxF.height = window.innerHeight * 0.50; // 80% of window height
            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxF.fillStyle = "red";
                ctxF.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }



            const cSa = document.getElementById("Saturday");
            const ctxSa = cSa.getContext("2d");
            //ctxSa.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxSa.height = window.innerHeight * 0.50; // 80% of window height
            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxSa.fillStyle = "red";
                ctxSa.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }



            const cSu = document.getElementById("Sunday");
            const ctxSu = cSu.getContext("2d");
            //ctxSu.width = window.innerWidth * 0.1419; // 80% of window width
            //ctxSu.height = window.innerHeight * 0.50; // 80% of window height
            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxSu.fillStyle = "red";
                ctxSu.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }
            //window.addEventListener('resize', domloaded);
        }
    function barPosition(dateTimeStart) {
        var date1 = new Date('2024-01-01T' + dateTimeStart + 'Z'); 
        var date2 = new Date('2024-01-01T' + `00:00:00` + 'Z');
        var differenceMs = date1.getTime() - date2.getTime();
        var hours = differenceMs / (1000 * 60 * 60);
        var pos = 150 * (hours/24);
        return pos;
    }

    function parceSize(dateTimeStart, dateTimeEnd){
        /*Range Date*/
        // Parse the time strings into Date objects
        var date1 = new Date('2024-01-01T' + dateTimeStart + 'Z'); 
        var date2 = new Date('2024-01-01T' + dateTimeEnd + 'Z');

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
            if(m.getDay == day) {
                MeetingsDay.push(m);
            }
          }
        return MeetingsDay;
    }


    

