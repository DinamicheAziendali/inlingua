// prepare "namespace"
window.bryntum = window.bryntum || {};
window.bryntum.locales = window.bryntum.locales || {};

// put the locale under window.bryntum.locales to make sure it is discovered automatically
window.bryntum.locales.It = {

  localeName: 'It',
  localeDesc: 'Italiano',

  // Translations for common words and phrases which are used by all classes.
  Object: {
    Yes: 'Si',
    No: 'No',
    Cancel: 'Annulla'
  },

  //region Columns

  TemplateColumn: {
    noTemplate: 'TemplateColumn non trova il template',
    noFunction: 'TemplateColumn.template deve essere una funzione'
  },

  ColumnStore: {
    columnTypeNotFound: function (data) {
      return 'Spalte typ ' + data.type + 'nicht registriert';
    }
  },

  //endregion

  //region Mixins

  InstancePlugin: {
    fnMissing: function (data) {
      return 'Trying to chain fn ' + data.plugIntoName + '#' + data.fnName + ', but plugin fn ' + data.pluginName + '#' + data.fnName + ' does not exist';
    },
    overrideFnMissing: function (data) {
      return 'Trying to override fn ' + data.plugIntoName + '#' + data.fnName + ', but plugin fn ' + data.pluginName + '#' + data.fnName + ' does not exist';
    }
  },

  //endregion

  //region Features

  ColumnPicker: {
    columnsMenu: 'Spalten',
    hideColumn: 'Versteck spalte',
    hideColumnShort: 'Versteck'
  },

  Filter: {
    applyFilter: 'Filter anwenden',
    filter: 'Filter',
    editFilter: 'Filter redigieren',
    on: 'Auf',
    before: 'Vor',
    after: 'Nach',
    equals: 'Gleichen',
    lessThan: 'Weniger als',
    moreThan: 'Mehr als',
    removeFilter: 'Filter entfernen'
  },

  FilterBar: {
    enableFilterBar: 'Filterleiste anzeigen',
    disableFilterBar: 'Filterleiste ausblenden'
  },

  Group: {
    groupAscending: 'Aufsteigend gruppieren',
    groupDescending: 'Absteigend gruppieren',
    groupAscendingShort: 'Aufsteigend',
    groupDescendingShort: 'Absteigend',
    stopGrouping: 'Stoppen gruppierung',
    stopGroupingShort: 'Stoppen'
  },

  Search: {
    searchForValue: 'Suche nach Wert'
  },

  Sort: {
    'sortAscending': 'Aufsteigend sortierung',
    'sortDescending': 'Absteigend sortierung',
    'multiSort': 'Multi sortieren',
    'removeSorter': 'Sortierung entfernen',
    'addSortAscending': 'Aufsteigend sortieren hinzufügen',
    'addSortDescending': 'Absteigend sortieren hinzufügen',
    'toggleSortAscending': 'Ändern Sie auf aufsteigend',
    'toggleSortDescending': 'Zu absteigend wechseln',
    'sortAscendingShort': 'Aufsteigend',
    'sortDescendingShort': 'Absteigend',
    'removeSorterShort': 'Entfernen',
    'addSortAscendingShort': '+ Aufsteigend',
    'addSortDescendingShort': '+ Absteigend'
  },

  Tree: {
    noTreeColumn: 'To use the tree feature one column must be configured with tree: true'
  },

  //endregion

  //region Grid

  Grid: {
    featureNotFound: function (data) {
      return 'Feature "' + data + '" not available, make sure you have imported it';
    },
    invalidFeatureNameFormat: function (data) {
      return 'Invalid feature name "' + data + '", must start with a lowercase letter';
    },
    removeRow: 'Rimuovi riga',
    removeRows: 'Rimuovi righe',
    loadFailedMessage: 'Wird geladen, bitte versuche es erneut',
    moveColumnLeft: 'Bewegen Sie sich zum linken Bereich',
    moveColumnRight: 'Bewegen Sie sich nach rechts'
  },

  GridBase: {
    loadMask: 'Caricamento in corso...',
    noRows: 'Nessun docente con lezioni programmate questa settimana'
  },

  //endregion

  //region Widgets

  Field: {
    invalidValue: 'Ungültiger Feldwert',
    minimumValueViolation: 'Mindestwertverletzung',
    maximumValueViolation: 'Maximalwertverletzung',
    fieldRequired: 'Dieses Feld wird benötigt',
    validateFilter: 'Der Wert muss aus der Liste ausgewählt werden'
  },

  DateField: {
    invalidDate: 'Ungültige Datumseingabe'
  },

  TimeField: {
    invalidTime: 'Ungültige Zeitangabe'
  },

  //endregion

  //region Others

  DateHelper: {
    locale: 'it',
    shortWeek: 'W',
    shortQuarter: 'q',
    week: 'Woche',
    weekStartDay: 0,
    unitNames: [
      { single: 'Millisecondo', plural: 'Millisecondi', abbrev: 'ms' },
      { single: 'Secondo', plural: 'Secondi', abbrev: 's' },
      { single: 'Minuto', plural: 'Minuti', abbrev: 'min' },
      { single: 'Stunde', plural: 'Stunden', abbrev: 'std' },
      { single: 'Giorno', plural: 'Giorni', abbrev: 't' },
      { single: 'Woche', plural: 'Wochen', abbrev: 'W' },
      { single: 'Monat', plural: 'Monathe', abbrev: 'mon' },
      { single: 'Quartal', plural: 'Quartal', abbrev: 'Q' },
      { single: 'Anno', plural: 'Anni', abbrev: 'jahr' }
    ],
    // Used to build a RegExp for parsing time units.
    // The full names from above are added into the generated Regexp.
    // So you may type "2 w" or "2 wk" or "2 week" or "2 weeks" into a DurationField.
    // When generating its display value though, it uses the full localized names above.
    unitAbbreviations: [
      ['mil'],
      ['s', 'sec'],
      ['m', 'min'],
      ['h', 'hr'],
      ['d'],
      ['w', 'wk'],
      ['mo', 'mon', 'mnt'],
      ['q', 'quar', 'qrt'],
      ['y', 'yr']
    ],
    parsers: {
      'L': 'DD.MM.YYYY',
      'LT': 'HH:mm'
    },
    ordinalSuffix: function (number) {
      return number;
    }
  },

  PagingToolbar: {
    firstPage: 'Gehe zur ersten Seite',
    prevPage: 'Zurück zur letzten Seite',
    page: 'Seite',
    nextPage: 'Gehe zur nächsten Seite',
    lastPage: 'Gehe zur letzten Seite',
    reload: 'Aktuelle Seite neu laden',
    noRecords: 'Keine Zeilen zum Anzeigen',
    pageCountTemplate: function (data) {
      return 'von ' + data.lastPage;
    },
    summaryTemplate: function (data) {
      return 'Ergebnisse ' + data.start + ' - ' + data.end + ' von ' + data.allCount;
    }
  },

  List: {
    loading: 'Beladung...'
  },

  //region Export

  PdfExport: {
    'Waiting for response from server...': 'Warten auf Antwort vom Server...'
  },

  ExportDialog: {
    width: '40em',
    labelWidth: '12em',
    exportSettings: 'Exporteinstellungen',
    export: 'Export',
    exporterType: 'Kontrolliere die Paginierung',
    cancel: 'Stornieren',
    fileFormat: 'Datei Format',
    rows: 'Reihen',
    alignRows: 'Zeilen ausrichten',
    columns: 'Säulen',
    paperFormat: 'Papierformat',
    orientation: 'Orientierung'
  },

  ExportRowsCombo: {
    all: 'Alle Zeilen',
    visible: 'Sichtbare Zeilen'
  },

  ExportOrientationCombo: {
    portrait: 'Porträt',
    landscape: 'Landschaft'
  },

  SinglePageExporter: {
    singlepage: 'Einzelne Seite'
  },

  MultiPageExporter: {
    multipage: 'Mehrere Seiten',
    exportingPage: function (data) {
      return 'Seite exportieren ' + data.currentPage + '/' + data.totalPages;
    }
  },

  //endregion

  //endregion

  //region Scheduler

  SchedulerCommon: {
    // SS              : 'AA',
    // SF              : 'EA',
    // FS              : 'AE',
    // FF              : 'EE',
    // StartToStart    : 'Inizio-Inizio',
    // StartToEnd      : 'Inizio-Fine',
    // EndToStart      : 'Enge-Inizio',
    // EndToEnd        : 'Enge-Fine',
    // dependencyTypes : [
    //     'AA',
    //     'EA',
    //     'AE',
    //     'EE'
    // ],
    // dependencyTypesLong : [
    //     'Inizio-Inizio',
    //     'Inizio-Fine',
    //     'Enge-Inizio',
    //     'Enge-Fine'
    // ]
  },

  ExcelExporter: {
    'No resource assigned': 'Keine Ressource zugewiesen'
  },

  ResourceInfoColumn: {
    eventCountText: function (data) {
      return data + ' Veranstaltung' + (data !== 1 ? 'en' : '');
    }
  },

  Dependencies: {
    from: 'Von',
    to: 'Zo',
    valid: 'Gültig',
    invalid: 'Ungültig',
    Checking: 'Überprüfung…'
  },

  DependencyEdit: {
    From: 'Da',
    To: 'a',
    Type: 'Tipo',
    Lag: 'Verzögern',
    'Edit dependency': 'Modifica dipendenza',
    Save: 'Salva',
    Delete: 'Elimina',
    Cancel: 'Annulla',
    StartToStart: 'Inizio-Inizio',
    StartToEnd: 'Inizio-Fine',
    EndToStart: 'Fine-Inizio',
    EndToEnd: 'Fine-Fine'
  },

  EventEdit: {
    Name: 'Nome',
    Resource: 'Risorsa',
    Start: 'Inizio',
    End: 'Fine',
    Save: 'Salva',
    Delete: 'Elimina',
    Cancel: 'Annulla',
    'Edit Event': 'Modifica evento',
    Repeat: 'Ripeti'
  },

  EventDrag: {
    eventOverlapsExisting: 'Ereignis überlappt vorhandenes Ereignis für diese Ressource',
    noDropOutsideTimeline: 'Event wird möglicherweise nicht vollständig außerhalb der Timeline gelöscht'
  },

  Scheduler: {
    'Add event': 'Aggiungi evento',
    'Delete event': 'Elimina evento',
    'Unassign event': 'Rimuovi assegnazione evento'
  },

  HeaderContextMenu: {
    pickZoomLevel: 'Zoom',
    activeDateRange: 'Datumsbereich',
    startText: 'Iniziosdatum',
    endText: 'Endtermin',
    todayText: 'Heute'
  },

  EventFilter: {
    filterEvents: 'Aufgaben filtern',
    byName: 'Namentlich'
  },

  TimeRanges: {
    showCurrentTimeLine: 'Aktuelle Zeitleiste anzeigen'
  },

  PresetManager: {
    minuteAndHour: {
      topDateFormat: 'ddd DD.MM, HH:mm'
    },
    hourAndDay: {
      topDateFormat: 'ddd DD.MM'
    },
    weekAndDay: {
      displayDateFormat: 'HH:mm'
    }
  },

  RecurrenceConfirmationPopup: {
    'delete-title': 'Du löschst ein Ereignis',
    'delete-all-message': 'Möchten Sie alle Vorkommen dieses Ereignisses löschen?',
    'delete-further-message': 'Möchten Sie dieses und alle zukünftigen Vorkommen dieses Ereignisses oder nur das ausgewählte Vorkommen löschen?',
    'delete-further-btn-text': 'Alle zukünftigen Ereignisse löschen',
    'delete-only-this-btn-text': 'Nur dieses Ereignis löschen',

    'update-title': 'Sie ändern ein sich wiederholendes Ereignis',
    'update-all-message': 'Möchten Sie alle Vorkommen dieses Ereignisses ändern?',
    'update-further-message': 'Möchten Sie nur dieses Vorkommen des Ereignisses oder dieses und aller zukünftigen Ereignisse ändern?',
    'update-further-btn-text': 'Alle zukünftigen Ereignisse',
    'update-only-this-btn-text': 'Nur dieses Ereignis',

    'Yes': 'Ja',
    'Cancel': 'Abbrechen',

    width: 600
  },

  RecurrenceLegend: {
    // list delimiters
    ' and ': ' und ',
    // frequency patterns
    'Daily': 'Täglich',
    'Weekly on {1}': function (data) {
      return 'Wöchentlich am ' + data.days;
    },
    'Monthly on {1}': function (data) {
      return 'Monatlich am ' + data.days;
    },
    'Yearly on {1} of {2}': function (data) {
      return 'Jährlich am ' + data.days + ' von ' + data.months;
    },
    'Every {0} days': function (data) {
      return 'Alle ' + data.interval + ' Tage';
    },
    'Every {0} weeks on {1}': function (data) {
      return 'Alle ' + data.interval + ' Wochen am ' + data.days;
    },
    'Every {0} months on {1}': function (data) {
      return 'Alle ' + data.interval + ' Monate auf ' + data.days;
    },
    'Every {0} years on {1} of {2}': function (data) {
      return 'Alle ' + data.interval + ' Jahre auf ' + data.days + ' von ' + data.months;
    },
    // day position translations
    'position1': 'ersten',
    'position2': 'zweiten',
    'position3': 'dritten',
    'position4': 'vierten',
    'position5': 'fünften',
    'position-1': 'letzten',
    // day options
    'day': 'Tag',
    'weekday': 'Wochentag',
    'weekend day': 'Wochenend-Tag',
    // {0} - day position info ("the last"/"the first"/...)
    // {1} - day info ("Sunday"/"Monday"/.../"day"/"weekday"/"weekend day")
    // For example:
    //  "the last Sunday"
    //  "the first weekday"
    //  "the second weekend day"
    'daysFormat': function (data) {
      return data.position + ' ' + data.days;
    }
  },

  RecurrenceEditor: {
    'Repeat event': 'Ereignis wiederholen',
    'Cancel': 'Abbrechen',
    'Save': 'Speichern',
    'Frequency': 'Häufigkeit',
    'Every': 'Jede(n/r)',
    'DAILYintervalUnit': 'Tag',
    'WEEKLYintervalUnit': 'Woche am:',
    'MONTHLYintervalUnit': 'Monat',
    'YEARLYintervalUnit': 'Jahr in:',
    'Each': 'Jeder',
    'On the': 'Am',
    'End repeat': 'Fine',
    'time(s)': 'Zeit'
  },

  RecurrenceDaysCombo: {
    'day': 'Tag',
    'weekday': 'Wochentag',
    'weekend day': 'Wochenend-Tag'
  },

  RecurrencePositionsCombo: {
    'position1': 'ersten',
    'position2': 'zweiten',
    'position3': 'dritten',
    'position4': 'vierten',
    'position5': 'fünften',
    'position-1': 'letzten'
  },

  RecurrenceStopConditionCombo: {
    'Never': 'Niemals',
    'After': 'Nach',
    'On date': 'Am Tag'
  },

  RecurrenceFrequencyCombo: {
    'Daily': 'täglich',
    'Weekly': 'wöchentlich',
    'Monthly': 'monatlich',
    'Yearly': 'jährlich'
  },

  RecurrenceCombo: {
    'None': 'Nie',
    'Custom...': 'Benutzerdefiniert ...'
  },

  //region Export

  ScheduleRangeCombo: {
    completeview: 'Vollständiger Zeitplan',
    currentview: 'Sichtbarer Zeitplan',
    daterange: 'Datumsbereich',
    completedata: 'Vollständiger Zeitplan (für alle Veranstaltungen)'
  },

  SchedulerExportDialog: {
    'Schedule range': 'Zeitplanbereich ',
    'Export from': 'Von',
    'Export to': 'Zu'
  },

  //endregion

  //endregion

  //region Examples

  Column: {
    'Name': 'Nome',
    'Age': 'Eta',
    'City': 'Città',
    'Food': 'Cibo',
    'Color': 'Colore',
    'First name': 'Nome',
    'Surname': 'Cognome',
    'Team': 'Team',
    'Score': 'Ergebnis',
    'Rank': 'Rang',
    'Percent': 'Percento',
    'Birthplace': 'Luogo di nascita',
    'Start': 'Inizio',
    'Finish': 'Fine',
    'Template': 'Modello',
    'Date': 'Data',
    'Check': 'Controlla',
    'Contact': 'Contatto',
    'Favorites': 'Preferiti',
    'Customer#': 'Cliente#',
    'When': 'Quando',
    'Brand': 'Marca',
    'Model': 'Modello',
    'Personal best': 'Persönlicher rekord',
    'Current rank': 'Aktueller rang',
    'Hometown': 'Heimatstadt',
    'Satisfaction': 'Zufriedenheit',
    'Favorite color': 'Lieblingsfarbe',
    'Rating': 'Wertung',
    'Cooks': 'Zuberaiten',
    'Birthday': 'Geburstag',
    'Staff': 'Personal',
    'Machines': 'Maschinen',
    'Type': 'Typ',
    'Task color': 'Aufgabe farbe',
    'Employment type': 'Beschäftigungsverhältnis',
    'Capacity': 'Kapazität',
    'Production line': 'Fließband',
    'Company': 'Firma',
    'End': 'Fine'
  },

  Shared: {
    'Locale changed': 'Sprache geändert'
  }

  //endregion

};
