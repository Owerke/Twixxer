function _all(q, e=document){return e.querySelectorAll(q)}
function _one(q, e=document){return e.querySelector(q)}


function toggleTweetModal(){
  _one("#tweetModal").classList.toggle("hidden")
}

async function sendTweet(){
  const form = event.target
  // Get the button, set the data-await, and disable it
  const button = _one("button[type='submit']", form)
  console.log(button)
  button.innerText = button.dataset.await
  // button.innerText = button.getAttribute("data-await")
  button.disabled = true
  const connection = await fetch("/api-create-tweet", {
    method : "POST",
    body : new FormData(form)
  })

  button.disabled = false
  button.innerText = button.dataset.default

  if( ! connection.ok ){
    return
  }
  const tweet_id = await connection.text() // tweet id will be here
  // Success
  let tweet = `
    <div id="${tweet_id}" class="p-4 border-t border-slate-200">
    <div class="flex">
      <img class="flex-none w-12 h-12 rounded-full" src="/images/1.jpg" alt="">
      <div class="w-full pl-4">
        <p class="font-bold">
          @xxx
        </p>            
        <p class="font-thin">
          aaa bbb
        </p>            
        <div class="pt-2">
          ${_one("input", form).value}
        </div>
        <div class="flex gap-12 w-full mt-4 text-lg">
            <i onclick="delete_tweet('${tweet_id}')" class="fas fa-trash ml-auto"></i>
            <i class="fa-solid fa-message"></i>
            <i class="fa-solid fa-heart"></i>
            <i class="fa-solid fa-retweet"></i>
            <i class="fa-solid fa-share-nodes"></i>
        </div>
      </div>
    </div>
  </div> 
  `
  _one("input", form).value = ""  

  _one("#tweets").insertAdjacentHTML("afterbegin", tweet)

}


async function delete_tweet(tweet_id){
  // Connect to the api and delete it from the "database"
  const connection = await fetch(`/api-delete-tweet/${tweet_id}`, {
    method : "DELETE"
  })
  if( ! connection.ok ){
    alert("uppps... try again")
    return
  }

  document.querySelector(`[id='${tweet_id}']`).remove()
}




