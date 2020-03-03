import pytest
from eanparser import EanParser


class TestEanParser:
    eanstring24 = '111122223333444455556666'
    eanstring13 = '1111122222333'
    otherlength = '12345678'
    nondigits = 'aaaaabbbbbccc'

    def test_eanparser_class_exists(self):
        eanparser = EanParser(self.eanstring13)
        assert isinstance(eanparser, EanParser)

    def test_ean_is_13_or_24_characters(self):
        eanparser24 = EanParser(self.eanstring24)
        assert isinstance(eanparser24, EanParser)
        eanparser13 = EanParser(self.eanstring13)
        assert isinstance(eanparser13, EanParser)

    def test_eanparser_raises_exception_with_other_string_length(self):
        with pytest.raises(ValueError) as e:
            EanParser(self.otherlength)
        assert 'Length of EAN is not 13 or 23' == str(e.value)

    def test_ean_is_a_string_with_only_numbers(self):
        with pytest.raises(ValueError) as e:
            EanParser(self.nondigits)
        assert 'EAN is not a numeric string' == str(e.value)

    def test_is_own_product_valid_ean(self):
        eanparser = EanParser('8480000278623')
        assert eanparser.isownproduct()

    def test_is_own_product_invalid_ean(self):
        eanparserinvalid = EanParser('848000027862300000000000')
        assert eanparserinvalid.isownproduct() == False, "This EAN can be only 13 characters, starting by '84'"

    def test_variable_weight_product_valid_ean(self):
        eanparser = EanParser('2369664001999')
        assert eanparser.isvariableweightproduct()

    def test_variable_weight_product_invalid_ean(self):
        eanparser = EanParser('238000027862300000000000')
        assert eanparser.isvariableweightproduct() == False, "This EAN can be only 13 characters, starting by '23'"

    def test_is_bulk_product_valid_ean(self):
        eanparser = EanParser('230036490033000165000542')
        assert eanparser.isbulkproduct()

    def test_is_bulk_product_invalid_ean(self):
        eanparser = EanParser('2369664001999')
        assert eanparser.isbulkproduct() == False, "This EAN can be only 24 characters, starting by '23'"

    def test_getmcode_for_own_product(self):
        eanparser = EanParser('8480000278623')
        assert eanparser.getmcode() == 27862

    def test_getmcode_for_variable_weight_product(self):
        eanparser = EanParser('2369664001999')
        assert eanparser.getmcode() == 69664

    def test_getmcode_for_bulk_product(self):
        eanparser = EanParser('230036490033000165000542')
        assert eanparser.getmcode() == 3649

    def test_getmcode_errors(self):
        eanparser = EanParser('840036490033000165000542')
        with pytest.raises(ValueError) as e:
            eanparser.getmcode()
        assert 'EAN does not belong to: own, variable weight, or bulk' == str(e.value)

    def test_getprice_for_var_weight_prod(self):
        eanparser = EanParser('2369664001999')
        assert eanparser.getprice() == 1.99

    def test_getprice_for_bulk_prod(self):
        eanparser = EanParser('230036490033000165000542')
        assert eanparser.getprice() == 0.54

    def test_getprice_for_no_price_prod(self):
        eanparser = EanParser('8480000278623')
        with pytest.raises(ValueError) as e:
            eanparser.getprice()
        assert 'EAN does not belong to variable weight or bulk prod' == str(e.value)

    def test_getpvp_for_bulk(self):
        eanparser = EanParser('230036490033000165000542')
        assert eanparser.getpvp() == 1.65

    def test_getpvp_for_non_bulk(self):
        eanparser = EanParser('8480000278623')
        with pytest.raises(ValueError) as e:
            eanparser.getpvp()
        assert 'EAN is not bulk prod' == str(e.value)

    def test_getweight_for_bulk(self):
        eanparser = EanParser('230036490033000165000542')
        assert eanparser.getweight() == 3.30

    def test_getweight_for_non_bulk(self):
        eanparser = EanParser('8480000278623')
        with pytest.raises(ValueError) as e:
            eanparser.getweight()
        assert 'EAN is not bulk prod' == str(e.value)
