
var result = []
function getMotivation(trueId) {
    (async () =>{
        const request = await fetch("https://private.proverki.gov.ru/erknm-catalogs/api/knm/"+trueId, {
          "headers": {
            "accept": "*/*",
            "accept-language": "ru,en;q=0.9",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
          },
          "referrer": "https://private.proverki.gov.ru/",
          "referrerPolicy": "origin",
          "body": null,
          "method": "GET",
          "mode": "cors",
          "credentials": "include"
        });
        const response = await request.json();
        result.push(response)
    })();
}

//var ids = resp['list'].map(function(n) {return n['id']})
var knms = [13013708, 13014199, 13360312, 13366758, 13683339, 13683426, 13693009, 13759294, 13759873, 13760483, 13764313, 13764457, 13764621, 13764953, 13799039, 13800633, 13800731, 13800792, 13804087, 13804698, 13804808, 13805019, 13805113, 13805211, 13805448, 13805810, 13822882, 13267239, 13267442, 13272683, 13273741, 13274069, 13274556, 13276928, 13278985, 13282155, 13285781, 13295318, 13295531, 13302456, 13302951, 13308818, 13309365, 13309911, 13310087, 13310305, 13310908, 13317151, 13317887, 13318228]   // Сюда номера проверок
var contents = []
function getFullKNM(trueId) {
    (async () =>{
        const req = await fetch("https://private.proverki.gov.ru/erknm-catalogs/api/knm/" + trueId, {
          "headers": {
            "accept": "*/*",
            "accept-language": "ru,en;q=0.9",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
          },
          "referrer": "https://private.proverki.gov.ru/",
          "referrerPolicy": "origin",
          "body": null,
          "method": "GET",
          "mode": "cors",
          "credentials": "include"
        });const res = await req.json();contents.push(res)
    })();
}
knms.forEach(n => getFullKNM(n));


function findAppealKnmFact() {

}