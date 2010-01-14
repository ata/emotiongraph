document.observe("dom:loaded", function() {
    FB.init("ead88d005b9905d8e6d13282e0065b93", "/xd_receiver.htm");
    $$('table tbody > tr:nth-child(even)').each(function(e){e.addClassName('even')})
});
