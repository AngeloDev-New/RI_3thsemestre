const h1 = document.createElement('h1')
const loading = load =>{
    document.getElementById('load').style.display = load
}
h1.classList.add('corpus_len')
fetch('/corpus')
.then(res => res.json())
.then(data => {
    h1.innerText = `O corpus conta com ${data['len']} arquivos`
    document.body.appendChild(h1)
})
const files_input = document.getElementById('files') 
files_input.addEventListener('change',e=>{
    loading(true)
    const files = e.target.files
    const form = new FormData()
    Array.from(files).forEach(file=>{
        form.append('files',file)
    })
    fetch('/corpus',{
        method:'POST',
        body:form
    }).then(res=>res.json())
    .then(data=>{
        loading(false)
        h1.innerText = `O corpus conta com ${data['len']} arquivos`
        console.log(data)
    }).catch(erro=>{
        loading(false)
        console.log(erro)
    }
)
})
document.getElementById('arquivos').addEventListener('click',()=>{
    files_input.click()
})