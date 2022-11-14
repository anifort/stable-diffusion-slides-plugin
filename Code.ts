const MAX_NUM_IMGS = 4;

const enum Orientation {
    LANDSCAPE = 'landscape',
    PORTRAIT = 'portrait',
    SQUARE='square'
}

const enum ImgColor {
    BLACK_AND_WHITE= 'bw',
    COLOR='colored'
}

const ImgColorPrompt = {
    [ImgColor.BLACK_AND_WHITE]: "in black and white",
    [ImgColor.COLOR]: "in color",
}

const enum ImgType {
    PHOTOGRAPH='photo',
    DRAWING='drawing',
    PAINTING='painting',
    SKETCH='sketch',
    ILLUSTRATION='illustration',
    GRAPHIC_DESIGN='graphicDesign'
}

const ImgTypePrompt = {
    [ImgType.PHOTOGRAPH]: "a photorealistic photograph of a ",
    [ImgType.DRAWING]: "a drawing of a ",
    [ImgType.PAINTING]: "a painting of a ",
    [ImgType.SKETCH]: "a sketch of a ",
    [ImgType.ILLUSTRATION]: "an illustration of a ",
    [ImgType.GRAPHIC_DESIGN]: "a graphic design of a ",
}

const enum ImgStyle {
    POP_ART='popArt',
    COMIC='comic',
    RETRO='retro',
    DISNEY='disney',
    VAN_GOGH='vanGogh',
    PICASSO='picasso',
    DALI='dali',
    YAYOI_KUSAMA = 'kusama'
}

const ImgStylePrompt = {
    [ImgStyle.POP_ART]: "in pop art style",
    [ImgStyle.COMIC]: "in comic style",
    [ImgStyle.RETRO]: "in retro style",
    [ImgStyle.DISNEY]: "in disney style, artstudio",
    [ImgStyle.VAN_GOGH]: "in Van Gogh style",
    [ImgStyle.PICASSO]: "in Pablo Picasso style",
    [ImgStyle.DALI]: "in Salvador Dali style",
    [ImgStyle.YAYOI_KUSAMA]: "in Yayoi Kusama style",
}

interface ImgOptions {
    description: string,
    numImgs: number,
    orientation: Orientation,
    imgColor: ImgColor,
    imgType: ImgType,
    imgStyle: ImgStyle
}

type Image = string;

interface AdvancedOptions {
    negativePrompt: string,
    seed: number,
    steps: number, 
    baseImg: Image
}

SlidesApp.getUi().createMenu("Image Generator")
                .addItem('Generate', 'showSidebar')
                .addToUi();

function showSidebar(){
    const ui = HtmlService
      .createHtmlOutputFromFile('sidebar')
      .setTitle('Image Generator');
  SlidesApp.getUi().showSidebar(ui);
}

function insertImgToSlide(imgUrl: string){
    const currentPage = SlidesApp.getActivePresentation().getSelection().getCurrentPage();
    currentPage.insertImage(imgUrl);
}
  
function generateImagesFromText(imgOptions: ImgOptions, advancedOptions: AdvancedOptions, savePrefs: boolean): string[] {

    if (savePrefs) {
        const userProperties = PropertiesService.getUserProperties();
        userProperties.setProperty('imgOptions', JSON.stringify(imgOptions));
        userProperties.setProperty('advancedOptions', JSON.stringify(advancedOptions));
    }
    return generateImagesFromTextInternal(imgOptions, advancedOptions)
}

  
function generateImagesFromTextInternal(imgOptions: ImgOptions, advancedOptions:AdvancedOptions):string[] {
//     Logger.log("in imageGenAPI");
//   // Call the API and return images 
//   var query = '"Apps Script" stars:">=100"';
//   var url = 'https://api.github.com/search/repositories'
//     + '?sort=stars'
//     + '&q=' + encodeURIComponent(query);

//   var response = UrlFetchApp.fetch(url, {'muteHttpExceptions': true});
//   Logger.log(response);
//   var json = response.getContentText();
//   var data = JSON.parse(json);
  
//   var html ='<div class="sidebar bottom"><img alt="Add-on logo" class="logo" src="https://www.dictionary.com/e/wp-content/uploads/2018/03/Thinking_Face_Emoji-Emoji-Island.png" width="27" height="27"><span class="gray branding-text">by the What If team</span></div>';
//   // turn into html

//   return html;
    return ["https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/0715034d-4044-4c55-9131-e4bfd6dd20ca/2_4x.png?format=2500w"]; 
}