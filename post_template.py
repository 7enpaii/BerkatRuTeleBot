def get_post(ad_post, post_index): 
    return f'''
{ad_post[post_index][0]}

╠═════════════════════════╣

{ad_post[post_index][1]}

╠═════════════════════════╣

{ad_post[post_index][2][0]}


{ad_post[post_index][2][1]}
{ad_post[post_index][2][2]}
{ad_post[post_index][2][3]}
{ad_post[post_index][2][4]}
{ad_post[post_index][2][5]}
{ad_post[post_index][2][6]}
{ad_post[post_index][2][7]}


П О С Т  № {post_index+1}
'''