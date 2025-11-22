const logo = document.getElementById('logo');
const queryContent = document.forms.query_form.query
queryContent.value = document.title

logo.addEventListener('click',()=>{
    window.location.href = '/';
})
const results = document.querySelectorAll('.result')
Array.from(results).forEach(result =>{
    result.addEventListener('click',e=>{
        const form = result.querySelector('form')
        form.submit()
    })
})