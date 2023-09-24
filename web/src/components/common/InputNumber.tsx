import { Input, InputProps } from 'antd'
import { NumericFormat, NumericFormatProps } from 'react-number-format'

interface IInputNumberProps
  extends Omit<
    NumericFormatProps<InputProps>,
    'value' | 'onChange' | 'onValueChange' | 'customInput' | 'defaultValue'
  > {
  value?: number
  onChange?: (value?: number) => void
}

export const InputNumber = (props: IInputNumberProps) => {
  const { value, onChange, ...restProps } = props
  return (
    <NumericFormat
      value={value}
      onValueChange={(d) => {
        onChange?.(d.floatValue)
      }}
      customInput={Input}
      {...restProps}
    />
  )
}
