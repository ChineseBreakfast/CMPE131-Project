// From this video https://www.youtube.com/watch?v=o1yMqPyYeAo

const date = new Date();

const renderCalendar = () => {
    
    date.setDate(1);

    const monthDays = document.querySelector(".days");
 
    const lastDay = new Date(date.getFullYear(),date.getMonth()+1,0).getDate();

    const prevLastDay = new Date(date.getFullYear(),date.getMonth(),0).getDate();

    const lastDayIndex = new Date( date.getFullYear(), date.getMonth() + 1, 0 ).getDay();

    const firstDayIndex = date.getDay();

    const nextDays = 7 - lastDayIndex -1 ;

    const months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];


    document.querySelector(".date h1").innerHTML = months[date.getMonth()] + " " + date.getFullYear();
    document.querySelector(".date p").innerHTML = new Date().toDateString();

    let days = "";

    for (let x = firstDayIndex; x > 0; x--){
        days += `<div class = "prev-date">${prevLastDay-x+1}</div>`;
    }

    for(let i = 1; i <= lastDay; i++) {
        if (i === new Date().getDate() && date.getMonth() === new Date().getMonth()) {
            days += `<div class = "today">${i}</div>`;
        }
        else {
            days += `<div>${i}</div>`;
        }
    }
    if (nextDays != 0){
        for (let j = 1; j <= nextDays; j++){
            
            days += `<div class = "next-date">${j}</div>`;
           
        }
    }
    monthDays.innerHTML = days; 
};

document.querySelector('.days ').addEventListener('click', function(e) {
    e = e || window.event;
    var target = e.target || e.srcElement,
    text = target.textContent || target.innerText; 
    name = target.className;
    if (target.className == "prev-date"){
        date.setMonth(date.getMonth()-1);
    }
    if (target.className == "next-date"){
        date.setMonth(date.getMonth()+1);
    }  
    year = date.getFullYear();
    month = date.getMonth();
    day = parseInt(text);
    let a = 1;
}, false);


document.querySelector('.prev ').addEventListener('click',() => {
    date.setMonth(date.getMonth()-1);
    if (date.getMonth() == 0)
        date.setFullYear(date.getFullYear()-1);
    renderCalendar();
});
document.querySelector('.next').addEventListener('click',() => {
    date.setMonth(date.getMonth()+1);
    if (date.getMonth() == 12)
        date.setFullYear(date.getFullYear()+1);
    renderCalendar();
});



renderCalendar();