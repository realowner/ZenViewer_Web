const listContentTabs = document.querySelectorAll('.tabcontent');
const listTabs = document.querySelectorAll('.tablinks');

listTabs.forEach(item=>{
    item.addEventListener('click', function (e) {
       openLogs(item.innerHTML);
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

function openLogs(logName) {
    listContentTabs.forEach(item => {
        if(item.dataset.id === logName) {
          item.classList.add('active')
        }
        else {
            item.classList.remove('active')
        }
    })
}
