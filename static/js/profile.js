"use strict";

const jwt = getJWTFromCookie();
const jwt_data = parseJwt(jwt);


async function deleteTweet(tweet_id) {
    console.log(tweet_id);
    // Connect to the api and delete it from the "database"
    const connection = await fetch(`/api/tweet/${tweet_id}`, {
        method: "DELETE",
        headers: {
            'Authorization': `Bearer ${jwt}`
        }
    });
    if (!connection.ok) {
        alert("uppps... try again");
        return;
    }

    document.getElementById(`tweet-${tweet_id}`).remove();
}

function htmlAddTweetToFeed(tweet, position = "beforeend") {
    let banner = "";
    if (tweet.banner_id != ""){
        banner = `<img id="tweet-banner-${tweet.banner_id} class="mt-2 w-full object-cover h-80" src="/static/tweet-banners/${tweet.banner_id}">`;
    }
    let deleteIcon = "";
    if (jwt_data.username == tweet.username) {
        deleteIcon = `<button type='button' onclick="deleteTweet('${tweet.id}')"><i class="cursor-pointer fa-solid fa-trash-can"></i></button>`;
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
                    <button type='button' onclick="" class="ml-auto"><i class="cursor-pointer fa-solid fa-message"></i></button>
                    <button type='button' onclick=""><i class="cursor-pointer fa-solid fa-heart"></i></button>
                    <button type='button' onclick=""><i class="cursor-pointer fa-solid fa-retweet"></i></button>
                    <button type='button' onclick=""><i class="cursor-pointer fa-solid fa-share-nodes"></i></button>
                    ${deleteIcon}
                </div>
            </div>
        </div>
    </div>
    `;

    let tweetsDiv = document.getElementById("tweets");
    // https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML
    tweetsDiv.insertAdjacentHTML(position, htmlTweetTemplate);
}


function htmlDisplayTweets(tweets) {
    for (let i = 0; i < tweets.length; i++) {
        const tweet = tweets[i];
        htmlAddTweetToFeed(tweet, "beforeend");
    }
}

async function get_tweets_for_user_by_username(username) {
    // Connect to the api and get all the tweets from the database
    //TODO fix user name <username> instead of
    const connection = await fetch(`/api/tweets/${username}`, {
        method: "GET",
        headers: {
            'Authorization': `Bearer ${jwt}`
        }
    });
    if (!connection.ok && !connection.status == 404) {
        alert("uppps...try again");
        return;
    }
    // Parse the string into a json
    const tweets = JSON.parse(await connection.text());
    // Display tweets
    htmlDisplayTweets(tweets);
}

async function submitTweet() {
    let tweet_content = document.getElementById("txt-tweet").value;

    const tweet = {
        "content": tweet_content,
        "banner_id": ""
    };

    const connection = await fetch(`/api/tweet`, {
        method: "POST",
        headers: {
            'Authorization': `Bearer ${jwt}`,
            'Content-Type': 'application/json'
        },

        body: JSON.stringify(tweet)
    });
    if (!connection.ok) {
        alert("uppps... try again");
        return;
    }
    const createdTweet = JSON.parse(await connection.text());
    htmlAddTweetToFeed(createdTweet, "afterbegin");

}

let path = window.location.pathname.split("/")
get_tweets_for_user_by_username(path[2]);
