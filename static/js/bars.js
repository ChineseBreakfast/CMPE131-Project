        
    document.addEventListener('DOMContentLoaded',domloaded,false);
    function domloaded(){

            const cM = document.getElementById("Monday");
            const ctxM = cM.getContext("2d");

            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxM.fillStyle = "red";
                ctxM.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }

            

            const cT = document.getElementById("Tuesday");
            const ctxT = cT.getContext("2d");

            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxT.fillStyle = "red";
                ctxT.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }



            const cW = document.getElementById("Wednesday");
            const ctxW = cW.getContext("2d");

            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxW.fillStyle = "red";
                ctxW.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }



            const cTh = document.getElementById("Thursday");
            const ctxTh = cTh.getContext("2d");

            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxTh.fillStyle = "red";
                ctxTh.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }



            const cF = document.getElementById("Friday");
            const ctxF = cF.getContext("2d");

            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxF.fillStyle = "red";
                ctxF.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }



            const cSa = document.getElementById("Saturday");
            const ctxSa = cSa.getContext("2d");

            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxSa.fillStyle = "red";
                ctxSa.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }



            const cSu = document.getElementById("Sunday");
            const ctxSu = cSu.getContext("2d");

            x = 200;
            offset = 0;
            for (let i = 0; i < 3; i++) {
                ctxSu.fillStyle = "red";
                ctxSu.fillRect(20, offset, x, 5);
                offset = offset + 6;
            }
        }
    function parceSize(){
        /*Range Date*/
    }
    function getWeek() {
        //default {}
            const d = new Date();
            let day = d.getDay();
        
    }
    function parceMeetingTimes() {

    }


    

