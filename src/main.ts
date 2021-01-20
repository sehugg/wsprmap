
const BANDS = ['m1','0','1','3','7','10','14','18','21','28','50','144']
const TXDBMS = ['0','3','7','10','13','17','20','23','27','30','33','37','40','43','47','50','53','57','60']
const HOURS = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
const MONTHS = ['12']

var viewlists = {
    month: MONTHS,
    hour: HOURS,
    band: BANDS,
    txdbm: TXDBMS
}

var viewopts = {
    year: '2020',
    month: '12',
    hour: '00',
    band: '10',
    txdbm: '23',
}

function refreshImage() {
    var imgpath = `output/map-${viewopts.year}-${viewopts.month}-${viewopts.hour}-${viewopts.band}-${viewopts.txdbm}.png`;
    (document.getElementById('mainimg') as HTMLImageElement).src = imgpath;
    console.log(imgpath);
}

function optionChanged(ev: Event) {
    viewopts.month = (document.getElementById('sel_month') as HTMLSelectElement).value;
    viewopts.hour = (document.getElementById('sel_hour') as HTMLSelectElement).value;
    viewopts.band = (document.getElementById('sel_band') as HTMLSelectElement).value;
    viewopts.txdbm = (document.getElementById('sel_txdbm') as HTMLSelectElement).value;
    refreshImage();
}

function incDecOption(name: string, delta: number) {
    return () => {
        var list = viewlists[name];
        var index = list.indexOf(viewopts[name]);
        index = (index + delta + list.length) % list.length;
        viewopts[name] = list[index];
        (document.getElementById('sel_'+name) as HTMLSelectElement).value = list[index];
        refreshImage();
    }
}

function populateSelector(name: string, values: any[], selected: any) {
    var div = document.getElementById('div_'+name) as HTMLElement;
    var el = document.getElementById('sel_'+name) as HTMLSelectElement;
    el.innerHTML = '';
    for (var val of values) {
        var opt = document.createElement('option');
        opt.text = val;
        opt.value = val;
        if (val+'' == selected+'') opt.selected = true;
        el.appendChild(opt);
    }
    el.addEventListener('change', optionChanged);
    var left = document.createElement('a');
    left.innerText = "<<";
    left.href = '#';
    left.onclick = incDecOption(name, -1);
    div.insertBefore(left, el);
    var right = document.createElement('a');
    right.innerText = ">>";
    right.href = '#';
    right.onclick = incDecOption(name, 1);
    div.appendChild(right);
}

populateSelector('month', MONTHS, viewopts.month);
populateSelector('hour', HOURS, viewopts.hour);
populateSelector('band', BANDS, viewopts.band);
populateSelector('txdbm', TXDBMS, viewopts.txdbm);
refreshImage();
