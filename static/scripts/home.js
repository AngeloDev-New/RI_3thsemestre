const h1 = document.createElement('h1')
let corpus_lenth = 0
const loading = load =>{ 
    const load_div = document.getElementById('load')
    if (load){
        load_div.style.display = 'flex';
    }else{
        load_div.style.display = 'none';

    }
}
h1.classList.add('corpus_len')
fetch('/corpus')
.then(res => res.json())
.then(data => {
    corpus_lenth += parseInt(data['len'])
    h1.innerText = `O corpus conta com ${corpus_lenth} arquivos`
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
        corpus_lenth += parseInt(data['len'])
        h1.innerText = `O corpus conta com ${corpus_lenth} arquivos`
        alert(`${data['qtd_arquivos']} arquivos submetidos,\n${data['len']} suportados\n${data['nao_suportados']} rejeitados`)
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