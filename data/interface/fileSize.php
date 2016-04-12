<?php
$GLOBALS['defaultMediaAssetPath'] = 'https://d2vt09yn8fcn7w.cloudfront.net';
$prefix = $GLOBALS['defaultMediaAssetPath'];
$file = file_get_contents('data.json');
$data = json_decode($file);
$clipCount = count($data->items);
$total = 0;
shellprint('Total clips: '.$clipCount);

$i = 1;
foreach($data->items as $clip){
	$asset = getSmallestAsset(json_decode($clip->assets, true), 256, 256);
	if($asset){
		$url = $prefix.$asset['src'];
		$size = curl_get_file_size($url);
		$total += $size;

		shellprint($i.'/'.$clipCount.': '.formatBytes($size).' ('.formatBytes($total).')');
		
		file_put_contents('files/'.$clip->id.'.mp4', fopen($url, 'r'));
		
	} else {
		shellprint($i.'/'.$clipCount.': No asset found!');
	}

	$i++;
	if($i > 30){
		break;
	}
}

shellprint('TOTAL FILESIZE = '.formatBytes($total));


function getSmallestAsset($assets, $width, $height){
	if(!$assets){ return false; }
	usort($assets, "cmp");
	foreach($assets as $asset){
		if($asset['width'] >= $width && $asset['height'] >= $height && $asset['mediatype'] != 'IMAGESEQUENCE'){
			return $asset;
		}
	}
}

function cmp($a, $b){
	if($a['height'] > $b['height']){
		return 1;
	} else if($a['height'] == $b['height']){
		return 0;
	} else {
		return -1;
	}
}

/**
 * Returns the size of a file without downloading it, or -1 if the file
 * size could not be determined.
 *
 * @param $url - The location of the remote file to download. Cannot
 * be null or empty.
 *
 * @return The size of the file referenced by $url, or -1 if the size
 * could not be determined.
 */
function curl_get_file_size( $url ) {
  // Assume failure.
  $result = -1;

  $curl = curl_init( $url );

  // Issue a HEAD request and follow any redirects.
  curl_setopt( $curl, CURLOPT_NOBODY, true );
  curl_setopt( $curl, CURLOPT_HEADER, true );
  curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
  curl_setopt( $curl, CURLOPT_FOLLOWLOCATION, true );

  $data = curl_exec( $curl );
  curl_close( $curl );

  if( $data ) {
    $content_length = "unknown";
    $status = "unknown";

    if( preg_match( "/^HTTP\/1\.[01] (\d\d\d)/", $data, $matches ) ) {
      $status = (int)$matches[1];
    }

    if( preg_match( "/Content-Length: (\d+)/", $data, $matches ) ) {
      $content_length = (int)$matches[1];
    }

    // http://en.wikipedia.org/wiki/List_of_HTTP_status_codes
    if( $status == 200 || ($status > 300 && $status <= 308) ) {
      $result = $content_length;
    }
  }

  return $result;
}

function formatBytes($bytes){ 
    return number_format($bytes / 1048576, 2).' MB';
}

function shellprint($string){
    echo($string . "\n");
}
?>