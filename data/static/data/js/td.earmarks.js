$().ready(function() {
	
	TD.EarmarksFilter = new TD.DataFilter();
	
	TD.EarmarksFilter.path = 'earmarks';
	TD.EarmarksFilter.ignoreForBulk = ['year'];
	
	TD.EarmarksFilter.row_content = function(row) {
		var content = '<td class="fiscal_year">' + row.fiscal_year + '</td>';
        content += '<td class="final_amount">$' + TD.Utils.currencyFormat(row.final_amount) + '</td>';
        content += '<td class="location">' + row.locations + '</td>';
        content += '<td class="description">' + row.description + '</td>';
        content += '<td class="members">' + row.members + '</td>';
        return content;
	};
	
	TD.EarmarksFilter.init = function() {
		
		TD.EarmarksFilter.registerFilter({
			name: 'amount',
			label: 'Amount',
			help: 'The final amount of the earmark.',
			field: TD.DataFilter.OperatorField
		});
		
		TD.EarmarksFilter.registerFilter({
			name: 'bill',
			label: 'Bill',
			help: 'The bill, section or subsection of the earmark.',
			field: TD.DataFilter.TextField,
			allowMultipleFields: true
		});
		
		TD.EarmarksFilter.registerFilter({
            name: 'description',
            label: 'Description',
            help: 'The description of the earmark request.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });
		
		TD.EarmarksFilter.registerFilter({
			name: 'recipient',
			label: 'Recipient',
			help: 'The intended recipient, when known.',
			field: TD.DataFilter.TextField,
			allowMultipleFields: true
		});
		
		TD.EarmarksFilter.registerFilter({
			name: 'city',
			label: 'Recipient City',
			help: 'The city where the money will be spent.',
			field: TD.DataFilter.TextField,
			allowMultipleFields: true
		});
		
		TD.EarmarksFilter.registerFilter({
			name: 'state',
			label: 'Recipient State',
			help: 'The state where the money will be spent.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: TD.STATES
		});
		
		TD.EarmarksFilter.registerFilter({
			name: 'member',
			label: 'Member Name',
			help: 'The name of the member requesting the earmark.',
			field: TD.DataFilter.TextField,
			allowMultipleFields: true
		});
		
		TD.EarmarksFilter.registerFilter({
			name: 'member_state',
			label: 'Member State',
			help: 'The state of the member requesting the earmark.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: TD.STATES
		});
		
		TD.EarmarksFilter.registerFilter({
			name: 'member_party',
			label: 'Member Party',
			help: 'The party of the member requesting the earmark.',
			field: TD.DataFilter.DropDownField,
			options: [['D', 'Democrat'], ['R', 'Republican']]
		});
		
        TD.EarmarksFilter.registerFilter({
            name: 'year',
            label: 'Fiscal Year',
            help: 'The fiscal year for which the earmark was requested.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [
				['', 'All'],
                ['2008','2008'],
                ['2009','2009'],
                ['2010','2010']
            ]
        });
		
		var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            TD.HashMonitor.setAnchor('year=2010');
            this.loadHash();
        }
        
        TD.EarmarksFilter.renumberFilters();
	};
});