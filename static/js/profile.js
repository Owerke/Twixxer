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
    let deleteIcon = "";
    if (jwt_data.username == tweet.username) {
        deleteIcon = `<button type='button' onclick="deleteTweet('${tweet.id}')"><i class="cursor-pointer fa-solid fa-trash-can"></i></button>`;
    }

    if (tweet.user_profile_picture_path == "") {
        tweet.user_profile_picture_path = "placeholder.png"
    }

    let htmlTweetTemplate = `
    <div id="tweet-${tweet.id}" class="p-4 border-t border-slate-200">
        <div class="flex">
            <img class="flex-none w-12 h-12 rounded-full" src="/static/images/profiles/${tweet.user_profile_picture_path}" alt="profile_pic">
            <div class="w-full pl-4">
                <p class="font-bold">
                    <a href='/profile/${tweet.username}'>@${tweet.username}</a> (Created at ${tweet.created})
                </p>
                <div class="pt-2">
                    ${tweet.content}
                </div>
                <div class="flex gap-12 w-full mt-4 text-lg">
                    <button type='button' onclick="" class="ml-auto"><i class="cursor-pointer fa-solid fa-message"></i></button>
                    ${deleteIcon}
                    <button type='button' onclick=""><i class="cursor-pointer fa-solid fa-heart"></i></button>
                    <button type='button' onclick=""><i class="cursor-pointer fa-solid fa-retweet"></i></button>
                    <button type='button' onclick=""><i class="cursor-pointer fa-solid fa-share-nodes"></i></button>
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

    for (let i = 0; i < tweets.length; i++) {
        const tweet = tweets[i]
        const connection = await fetch(`/api/user/${tweet.username}`, {
            method: "GET",
            headers: {
                'Authorization': `Bearer ${jwt}`
            }
        });
        if (!connection.ok) {
            alert("uppps...try again");
            return;
        }
        // Parse the string into a json
        const user = JSON.parse(await connection.text());
        tweets[i].user_profile_picture_path = user.picture_path;
    }


    // Display tweets
    htmlDisplayTweets(tweets);
}

async function submitTweet() {
    let tweet_content = document.getElementById("txt-tweet").value;

    const tweet = {
        "content": tweet_content
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

async function htmlDisplayFollowStatus(user) {
    const connection = await fetch(`/api/user/${user}/isfollowed`, {
        method: "GET",
        headers: {
            'Authorization': `Bearer ${jwt}`,
            'Content-Type': 'application/json'
        }
    });
    if (!connection.ok) {
        alert("uppps... try again");
        return;
    }
    const response = JSON.parse(await connection.text());
    let isFollowed = response.isFollowed;

    if (isFollowed) {
        document.getElementById("btn-follow").style.display = "none"
        document.getElementById("btn-unfollow").style.display = "block"
    } else {
        document.getElementById("btn-follow").style.display = "block"
        document.getElementById("btn-unfollow").style.display = "none"
    }

}

async function follow_user() {
    let user = window.location.pathname.split("/")[2]

    const connection = await fetch(`/api/user/${user}/follow`, {
        method: "POST",
        headers: {
            'Authorization': `Bearer ${jwt}`,
            'Content-Type': 'application/json'
        }
    });
    if (!connection.ok) {
        alert("uppps... try again");
        return;
    }

    htmlDisplayFollowStatus(user);
}

async function unfollow_user() {
    let user = window.location.pathname.split("/")[2]

    const connection = await fetch(`/api/user/${user}/follow`, {
        method: "DELETE",
        headers: {
            'Authorization': `Bearer ${jwt}`,
            'Content-Type': 'application/json'
        }
    });
    if (!connection.ok) {
        alert("uppps... try again");
        return;
    }

    htmlDisplayFollowStatus(user);
}

let path = window.location.pathname.split("/");
let username = path[2];

get_tweets_for_user_by_username(username);
htmlDisplayFollowStatus(username);
