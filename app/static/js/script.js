const listContentTabs = document.querySelectorAll('.tabcontent');
const listTabs = document.querySelectorAll('.tablinks');

listTabs.forEach(item=>{
    item.addEventListener('click', function (e) {
       openCity(item.innerHTML);
       activeTab(item.innerHTML)
    })
})

function activeTab(tabsName) {
    listTabs.forEach(item => {
        if(item.innerHTML === tabsName) {
            item.classList.add('tab-active')
        }
        else {
            item.classList.remove('tab-active');
        }
    })
}

function openCity(cityName) {
    listContentTabs.forEach(item => {
        if(item.dataset.id === cityName) {
          item.classList.add('active')
        }
        else {
            item.classList.remove('active')
        }
    })
}