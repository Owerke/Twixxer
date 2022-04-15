"use strict";

let jwt = ""

function getCookie(cname) {
    // Source: https://www.w3schools.com/js/js_cookies.asp
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

function parseJwt (token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};

function getJWTFromCookie() {
    return getCookie("user_session_jwt")
}

async function delete_tweet(tweet_id) {
    // Connect to the api and delete it from the "database"
    const connection = await fetch(`/api-delete-tweet/${tweet_id}`, {
        method: "DELETE"
    })
    if (!connection.ok) {
        alert("uppps... try again")
        return
    }

    document.querySelector(`[id='${tweet_id}']`).remove()
}

function htmlDisplayTweets(tweets, username="") {
    let tweetsDiv = document.getElementById("tweets");

    for (let i = 0; i < tweets.length; i++) {
        const tweet = tweets[i];
        let banner = ""
        if (tweet.banner_id != ""){
            banner = `<img id="tweet-banner-${tweet.banner_id} class="mt-2 w-full object-cover h-80" src="/static/tweet-banners/${tweet.banner_id}">`
        }
        let deleteIcon = ""
        if (username == tweet.username) {
            deleteIcon = `<i class="fa-solid fa-trash-can"></i>`
        }


        let htmlTweetTemplate = `
        <div id="tweet-${tweet.id}" class="p-4 border-t border-slate-200">
            <div class="flex">
                <img class="flex-none w-12 h-12 rounded-full" src="/static/images/placeholder.png" alt="profile_pic">
                <div class="w-full pl-4">
                    <p class="font-bold">
                        @${tweet.username} (Created at ${tweet.created})
                    </p>
                    <p class="font-thin">
                        ${tweet.username}
                    </p>
                    <div class="pt-2">
                        ${tweet.content}
                    </div>
                        ${banner}
                    <div class="flex gap-12 w-full mt-4 text-lg">
                        <i class="fa-solid fa-message ml-auto"></i>
                        <i class="fa-solid fa-heart"></i>
                        <i class="fa-solid fa-retweet"></i>
                        <i class="fa-solid fa-share-nodes"></i>
                        ${deleteIcon}
                    </div>
                </div>
            </div>
        </div>
        `
        tweetsDiv.insertAdjacentHTML("beforeend", htmlTweetTemplate)
    }
}

async function getTweets() {
    const jwt = getJWTFromCookie()
    const jwt_data = parseJwt(jwt)
    // Set authentication header to JWT, so we can do stuff.
    let myHeaders = new Headers();
    myHeaders.set('Authorization', 'Bearer ' + jwt);

    // Connect to the api and get all the tweets from the database
    const connection = await fetch(`/api/tweets`, {
        method: "GET",
        headers: myHeaders
    })
    if (!connection.ok) {
        alert("uppps...try again")
        return
    }
    // Parse the string into a json
    const tweets = JSON.parse(await connection.text())
    // Display tweets
    htmlDisplayTweets(tweets, jwt_data.username)
}

getTweets()
