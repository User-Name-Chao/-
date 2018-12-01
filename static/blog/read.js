
$(function () {
    $('.blogtitle').click(function () {
        var title=$(this).attr('title');
        var content=$(this).parents('div').next().attr('content');
        $getJson('/blog/read/',{'title':title,'content':content},function () {
            
        })
        
    })
})









































