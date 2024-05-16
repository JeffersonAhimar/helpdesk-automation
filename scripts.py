def scriptChangeTicketStatus():
    return """
    // UPDATE STATUS -> Resuelto
    const cbStatus = document.getElementById('STATUSID');
    cbStatus.value = '4';

    // UPDATE Motivo (if=='0') -> No Aplica
    const cbMotivo = document.querySelector('select[name="WorkOrder_Fields_UDF_CHAR25"]')
    if (cbMotivo.value == '0') {
        cbMotivo.value = 'No Aplica'
    }

    // Open Resolution
    toggleResolution();

    setTimeout(() => {
        // Set Resolution
        const iframeElement = document.querySelector('#resolutionBox table tbody tr td div .rv-nvalues div table tbody tr td div iframe')
        const iframeContent = iframeElement.contentDocument || iframeElement.contentWindow.document;
        const ze_body = iframeContent.querySelector('body');
        ze_body.innerHTML = 'Resuelto'
        // Send form
        const btnSubmitRequest = document.getElementById('updateWOButton');
        btnSubmitRequest.click();
    }, 500);
    """