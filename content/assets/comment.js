function addcomment(){
comment=document.getElementById('com1').value;
comments = '<li class="photo__comment"><span class="photo__comment-author">ritik</span> love this!</li><li class="photo__comment"><span class="photo__comment-author">vrishabh</span> nice</li><li class="photo__comment"><span class="photo__comment-author">Vrishab</span>'+' '+comment+'</li>';
document.getElementById('coms1').innerHTML = comments;
}

function addcomment2(){
comment=document.getElementById('com2').value;
comments = '<li class="photo__comment"><span class="photo__comment-author">ritik</span> love this!</li><li class="photo__comment"><span class="photo__comment-author">vrishabh</span> nice</li><li class="photo__comment"><span class="photo__comment-author">Vrishab</span>'+' '+comment+'</li>';
document.getElementById('coms2').innerHTML = comments;
}